use axum::{
    extract::Extension,
    routing::get,
    Router,
    serve,
    Json
};

use serde_json::json;
use std::{sync::{Arc, atomic::{Ordering, AtomicUsize}}};
use tokio::net::TcpListener;
use tower::ServiceBuilder;

mod utils;

#[tokio::main]
async fn main() {
    let counter = Arc::new(AtomicUsize::new(0));

    let app = Router::new()
        .route("/", get(handler)) // not needed?
        .route("/pingpong", get({
            let counter = Arc::clone(&counter);
            move || utils::ping_logger(Arc::clone(&counter))
        }))
        .route("/pings", get({
            let counter = Arc::clone(&counter);
            move || get_pings(counter)
        }))
        .layer(ServiceBuilder::new().layer(Extension(counter)));

    let listener = TcpListener::bind("0.0.0.0:8089").await.unwrap();
    serve(listener, app).await.unwrap();
}

async fn handler(
    Extension(counter): Extension<Arc<AtomicUsize>>,
) -> String {
    let count = counter.fetch_add(1, Ordering::SeqCst) + 1;
    format!("Pong {}", count)
}

async fn get_pings(counter: Arc<AtomicUsize>) -> Json<serde_json::Value> {
    let count = counter.load(Ordering::Relaxed);
    Json(json!({ "count": count }))
}