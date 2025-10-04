package main

import (
"fmt"
"net/http"
)

func main() {
http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, {"status": "healthy"})
})
http.ListenAndServe(":8080", nil)
}
