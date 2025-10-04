variable "replicas" { type = number, default = 1 }
output "bootstrap_servers" { value = "localhost:9092" }
