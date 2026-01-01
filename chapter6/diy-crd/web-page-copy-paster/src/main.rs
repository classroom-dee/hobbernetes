/// TODO: Expose port in dep and build a service too

use futures::StreamExt;
use kube::{
    api::{Api, Patch, PatchParams},
    runtime::controller::{Action, Controller},
    Client, CustomResource, ResourceExt,
};
use k8s_openapi::{
    api::{
        apps::v1::{Deployment, DeploymentSpec},
        core::v1::{Container, EnvVar, PodSpec, PodTemplateSpec},
    },
    apimachinery::pkg::apis::meta::v1::{LabelSelector, ObjectMeta},
};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use std::{collections::BTreeMap, sync::Arc, time::Duration};
use tracing::{error, info};


/// Typing
#[derive(CustomResource, Debug, Deserialize, Serialize, Clone, JsonSchema)]
#[kube(
    group = "stable.dwk",
    version = "v1",
    kind = "DummySite",
    plural = "dummysites",
    namespaced
)]
pub struct DummySiteSpec {
    pub website_url: String,
    pub image: String,
}


/// Context shared with reconcile + error
#[derive(Clone)]
struct Data {
    client: Client,
}


/// Main
#[tokio::main]
async fn main() -> Result<(), kube::Error> {
    tracing_subscriber::fmt::init();

    let client = Client::try_default().await?;
    let dummysites: Api<DummySite> = Api::all(client.clone());

    let context = Arc::new(Data { client });

    Controller::new(dummysites, Default::default())
        .run(reconcile, error_policy, context)
        .for_each(|res| async move {
            match res {
                Ok((obj_ref, _action)) => info!("reconciled: {:?}", obj_ref),
                Err(e) => error!("reconcile failed: {}", e),
            }
        })
        .await;

    Ok(())
}


/// Called whenever a DummySite is created/updated and on requeues
async fn reconcile(ds: Arc<DummySite>, ctx: Arc<Data>) -> Result<Action, kube::Error> {
    let client = ctx.client.clone();
    let ns = ds.namespace().unwrap_or_else(|| "default".to_string());
    let name = ds.name_any();

    // Desired Deployment name = DummySite name
    let desired = build_deployment(&ds, &ns);

    // create/update the Deployment
    let deployments: Api<Deployment> = Api::namespaced(client, &ns);

    // Server-side apply, idempotent
    let pp = PatchParams::apply("dummysite-controller").force();
    deployments
        .patch(&name, &pp, &Patch::Apply(&desired))
        .await?;

    info!("ensured Deployment/{name} in namespace {ns}");

    // Requeue for safety ... temp measure
    Ok(Action::requeue(Duration::from_secs(300)))
}


/// If reconcile errors, retry after a short delay
fn error_policy(_ds: Arc<DummySite>, _err: &kube::Error, _ctx: Arc<Data>) -> Action {
    Action::requeue(Duration::from_secs(10))
}


/// Build a Deployment that injects WEBSITE_URL into the container
fn build_deployment(ds: &DummySite, ns: &str) -> Deployment {
    let name = ds.name_any();
    let mut labels = BTreeMap::new();
    labels.insert("app".to_string(), name.clone());

    Deployment {
        metadata: ObjectMeta {
            name: Some(name.clone()),
            namespace: Some(ns.to_string()),
            ..Default::default()
        },
        spec: Some(DeploymentSpec {
            replicas: Some(1),
            selector: LabelSelector {
                match_labels: Some(labels.clone()),
                ..Default::default()
            },
            template: PodTemplateSpec {
                metadata: Some(ObjectMeta {
                    labels: Some(labels),
                    ..Default::default()
                }),
                spec: Some(PodSpec {
                    containers: vec![Container {
                        name: "sitecopier".to_string(),
                        image: Some(ds.spec.image.clone()),
                        env: Some(vec![EnvVar {
                            name: "WEBSITE_URL".to_string(),
                            value: Some(ds.spec.website_url.clone()),
                            ..Default::default()
                        }]),
                        ..Default::default()
                    }],
                    ..Default::default()
                }),
            },
            ..Default::default()
        }),
        ..Default::default()
    }
}
