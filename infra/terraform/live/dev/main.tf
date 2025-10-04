provider "kubernetes" { }
module "k8s" {
  source = "../../modules/k8s-cluster"
  cluster_name = "dev-cluster"
}
module "kafka" {
  source = "../../modules/kafka-cluster"
}
module "schema" {
  source = "../../modules/schema-registry"
}
module "mlflow" {
  source = "../../modules/mlflow"
}
module "mesh" {
  source = "../../modules/service-mesh"
}
output "kafka_bootstrap" { value = module.kafka.bootstrap_servers }
