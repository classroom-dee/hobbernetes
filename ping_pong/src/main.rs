use axum::{
    extract::Extension,
    routing::get,
    Router,
    serve,
    Json
};

use serde_json::json;
use std::{sync::{Arc, atomic::{Ordering, AtomicUsize}}, env};
use tokio::net::TcpListener;
use tower::ServiceBuilder;

mod utils;

#[tokio::main]
async fn main() {
    let counter = Arc::new(AtomicUsize::new(0));

    let app = Router::new()
        .route("/", get({ // /pingpong's root
            let counter = Arc::clone(&counter);
            move || utils::ping_logger(Arc::clone(&counter))
        }))
        .route("/pings", get({
            let counter = Arc::clone(&counter);
            move || get_pings(counter)
        }))
        .route("/pong", get(handler))
        .route("//pings", get({ // istio VS rewrite results in redundant slash. why python backends don't need this?
            let counter = Arc::clone(&counter);
            move || get_pings(counter)
        }))
        .route("//pong", get(handler))
        .layer(ServiceBuilder::new().layer(Extension(counter)))
        .fallback(|uri: axum::http::Uri| async move {format!("NO MATCH: {}", uri)});
        
    let port = env::var("PINGPONG_PORT").unwrap_or_else(|_| "8089".into());
    let addr = format!("0.0.0.0:{}", port);
    let listener = TcpListener::bind(&addr).await.unwrap();
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