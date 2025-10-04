FROM rust:1.71 as builder
WORKDIR /app
COPY . .
RUN cargo build --release
FROM debian:buster-slim
COPY --from=builder /app/target/release/service /usr/local/bin/service
CMD ["/usr/local/bin/service"]
