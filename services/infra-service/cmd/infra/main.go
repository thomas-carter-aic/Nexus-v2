package main
import (
  "encoding/json"
  "net/http"
  "log"
)
func main(){
  http.HandleFunc("/allocate", func(w http.ResponseWriter, r *http.Request){
    var req map[string]interface{}
    _ = json.NewDecoder(r.Body).Decode(&req)
    resp := map[string]interface{}{"resourceId":"res-123","status":"allocated"}
    w.Header().Set("Content-Type","application/json")
    json.NewEncoder(w).Encode(resp)
  })
  log.Println("infra-service listening :9100")
  http.ListenAndServe(":9100", nil)
}
