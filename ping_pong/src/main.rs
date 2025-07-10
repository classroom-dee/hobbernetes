use axum::{
    extract::Extension,
    routing::get,
    Router,
    serve,
};
use std::{
    sync::{Arc, atomic::{AtomicUsize, Ordering}},
};
use tokio::net::TcpListener;
use tower::ServiceBuilder;

#[tokio::main]
async fn main() {
    let counter = Arc::new(AtomicUsize::new(0));

    let app = Router::new()
        .route("/", get(handler))
        .route("/pingpong", get(handler))
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
