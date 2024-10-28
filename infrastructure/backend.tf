terraform {
  backend "s3" {
    bucket         = "fastapi-demo-app-terraform"
    key            = "terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
  }
}