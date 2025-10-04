FROM golang:1.20-alpine AS build
WORKDIR /src
COPY . .
RUN go build -o /out/service ./cmd/service
FROM alpine
COPY --from=build /out/service /usr/local/bin/service
ENTRYPOINT ["/usr/local/bin/service"]
