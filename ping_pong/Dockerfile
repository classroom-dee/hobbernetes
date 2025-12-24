# Trying to unburden the fat toolchain
FROM rust:1.81-slim AS builder
WORKDIR /app
COPY . .

# TODO: output clean log during workflow, not the package problem.
# TODO: add this flag to docker build in workflow : --progress=plain
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    musl-tools \
    build-essential \
    pkg-config \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && rustup target add x86_64-unknown-linux-musl \
    && cargo build --release --target x86_64-unknown-linux-musl

# Second stage for packing up
# 1GB to 5MB?? ... You can't not do this...
FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/ping-pong /ping-pong

ENTRYPOINT ["/ping-pong"]