FROM golang:1.20-alpine AS build
WORKDIR /src
COPY . .
RUN go build -o /out/orchestration ./cmd/orchestration
FROM alpine
COPY --from=build /out/orchestration /usr/local/bin/orchestration
ENTRYPOINT ["/usr/local/bin/orchestration"]
