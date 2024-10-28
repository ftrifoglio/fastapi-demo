variable "aws_region" {
  type = string
}
variable "app_name" {
  type = string
}
variable "ecr_repository_url" {
  type = string
}
variable "subnets" {
  type = list(string)
}
variable "vpc" {
  type = string
}
variable "image_tag" {
  type = string
}