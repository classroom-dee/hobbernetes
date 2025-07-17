use axum::{
    extract::Extension,
    routing::get,
    Router,
    serve,
    Json
};
use serde::{Serialize, Deserialize};
use serde_json::json;
use std::{
    fs::{OpenOptions},
    io::{BufReader, BufWriter},
    sync::{Arc, atomic::{AtomicUsize, Ordering}},
};
use tokio::net::TcpListener;
use tower::ServiceBuilder;
use std::sync::Mutex;

// could be expanded to a request logger?...
#[derive(Serialize, Deserialize)]
struct PingRecord {
    id: usize,
}

#[tokio::main]
async fn main() {
    let counter = Arc::new(AtomicUsize::new(0));
    let log_lock = Arc::new(Mutex::new(()));

    let app = Router::new()
        .route("/", get(handler)) // not needed?
        .route("/pingpong", get({
            let counter = Arc::clone(&counter);
            let log_lock = Arc::clone(&log_lock);
            move || ping_logger(Arc::clone(&counter), Arc::clone(&log_lock))
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

async fn ping_logger(
    counter: Arc<AtomicUsize>,
    file_lock: Arc<Mutex<()>>,
) -> String {
    let count = counter.fetch_add(1, Ordering::SeqCst) + 1;
    let record = PingRecord { id: count };

    let _guard = file_lock.lock().unwrap();

    let path = "/tmp/logs/pings.json";

    // load & push
    let mut list: Vec<PingRecord> = match std::fs::File::open(path) {
        Ok(file) => {
            let reader = BufReader::new(file);
            serde_json::from_reader(reader).unwrap_or_default()
        }
        Err(_) => Vec::new(),
    };

    list.push(record);

    // save
    let file = OpenOptions::new().write(true).create(true).truncate(true).open(path).unwrap();
    let writer = BufWriter::new(file);
    serde_json::to_writer_pretty(writer, &list).unwrap();

    format!("Pong {}", count)
}