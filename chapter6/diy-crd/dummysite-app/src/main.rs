use axum::{response::Html, routing::get, Router};
use regex::Regex;
use std::{env, net::SocketAddr, sync::Arc};
use tracing::{error, info};

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let url = env::var("WEBSITE_URL").unwrap_or_else(|_| {
        eprintln!("Missing WEBSITE_URL env var!");
        std::process::exit(1);
    });

    // Fetch once on startup and serve cached HTML (minimal PoC)
    let html = match fetch_and_simplify(&url).await {
        Ok(h) => h,
        Err(e) => {
            error!("failed to fetch {}: {}", url, e);
            format!("<html><body><h1>Fetch failed</h1><pre>{}</pre></body></html>", e)
        }
    };

    let shared = Arc::new(html);

    let app = Router::new().route(
        "/",
        get({
            let shared = shared.clone();
            move || async move { Html((*shared).clone()) }
        }),
    );

    let addr: SocketAddr = "0.0.0.0:3000".parse().unwrap();
    info!("serving on http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn fetch_and_simplify(url: &str) -> Result<String, reqwest::Error> {
    // Wikimedia requires a User-Agent header (and recommends it be informative). :contentReference[oaicite:4]{index=4}
    let client = reqwest::Client::builder()
        .user_agent("DummySitePoC/0.1 (k8s controller PoC)")
        .build()?;

    let mut html = client.get(url).send().await?.text().await?;

    // Remove inline CSS
    // (simple regex-based stripping for PoC; not a perfect HTML parser)
    let re_style = Regex::new(r"(?is)<style[^>]*>.*?</style>").unwrap();
    html = re_style.replace_all(&html, "").to_string(); // :contentReference[oaicite:5]{index=5}

    // Remove linked stylesheets
    let re_link_css = Regex::new(r#"(?is)<link[^>]*rel=["']?stylesheet["']?[^>]*>"#).unwrap();
    html = re_link_css.replace_all(&html, "").to_string(); // :contentReference[oaicite:6]{index=6}

    Ok(html)
}
