variable "credentials" {
  description = "My credentials"
  default = "./keys/mycreds.json"
}

variable "gcs_bucket" {
  description = "My Storage Bucket"
  default = "terraform-demo-447307-terra-bucket"
}

variable "project" {
  description = "My project"
  default = "terraform-demo-447307"
}

variable "location" {
  description = "My location"
  default = "US"
}

variable "region" {
  description = "My region"
  default = "us-central1"
}

variable "google_bigquery_dataset" {
  description = "My Big query dataset"
  default = "demo_dataset"
}

variable "gcs_storage_class" {
    description = "Bucket storage class"
    default = "STANDARD"
}