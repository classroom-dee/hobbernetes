# Trying to unburden the fat toolchain
FROM rust:1.78-slim AS builder
WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y musl-tools && rm -rf /var/lib/apt/lists/*

RUN rustup target add x86_64-unknown-linux-musl
RUN cargo build --release --target x86_64-unknown-linux-musl

# Second stage for packing up
# 1GB to 5MB?? ... You can't not do this...
FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/ping-pong /ping-pong

ENTRYPOINT ["/ping-pong"]