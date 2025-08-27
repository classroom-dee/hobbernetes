use std::{env, sync::{Arc, atomic::{Ordering, AtomicUsize}}};
use tokio_postgres::{NoTls, Error};

pub async fn ping_logger(
    counter: Arc<AtomicUsize>,
) -> String {
    let count = counter.fetch_add(1, Ordering::SeqCst) + 1;

    let user = env::var("DB_USER").unwrap_or_else(|_| "postgres".into());
    let pass = env::var("DB_PASS").unwrap_or_default();
    let host = env::var("DB_HOST").unwrap_or_else(|_| "127.0.0.1".into());
    let port: u16 = env::var("DB_PORT")
        .ok()
        .and_then(|p| p.parse().ok())
        .unwrap_or(5432);
    let dbname = env::var("DB_NAME").unwrap_or_else(|_| user.clone());


    let conn_str = format!(
        "host={} port={} user={} password={} dbname={}",
        host, port, user, pass, dbname
    );

    // transactions
    let result = async {
        // spawn io driver -> connection
        let (client, connection) = tokio_postgres::connect(&conn_str, NoTls).await?;
        tokio::spawn(async move {
            if let Err(e) = connection.await {
                eprintln!("postgres connection error: {e}");
            }
        });

        // create table if not exist
        // BIG SEREAL 🤣😂🤣
        client.execute(
            r#"
            CREATE TABLE IF NOT EXISTS pings (
                id           BIGSERIAL   PRIMARY KEY,
                sess_req_cnt BIGINT      NOT NULL,
                created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            "#,
            &[],
        ).await?;

        client
            .execute("INSERT INTO pings (sess_req_cnt) VALUES ($1)",
                &[&(count as i64)]
            )
            .await?;

        Ok::<(), Error>(())
    }
    .await;

    match result {
        Ok(()) => format!("Session request count {} - saved to DB.", count),
        Err(e) => format!("Pong {} - faled to save: {}", count, e),
    }
}