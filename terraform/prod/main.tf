locals {
  project_id = "my-playground-458212"
  location   = "asia-northeast1"
}

data "google_secret_manager_secret_version" "api_key_secret" {
  project = local.project_id
  secret  = "google-ai-studio-api-key"
  version = "latest"
}

data "google_secret_manager_secret_version" "line_channel_secret" {
  project = local.project_id
  secret  = "line-channel-secret-line-draw"
  version = "latest"
}

data "google_secret_manager_secret_version" "line_channel_access_token" {
  project = local.project_id
  secret  = "line-channel-access-token-line-draw"
  version = "latest"
}

module "workload_identity" {
  source            = "../module/workload_identity"
  project_id        = local.project_id
  github_repo_owner = "yamaguchi-milkcocholate"
  github_repo_name  = "gcp-line-developper"
}

module "cloud_run" {
  source                       = "../module/cloud_run"
  project_id                   = local.project_id
  location                     = local.location
  app_name                     = "managed-line-developper"
  artifact_registry_repo_name  = "docker-image-repo"
  artifact_registry_image_name = "line-draw"
  google_ai_studio_api_key     = data.google_secret_manager_secret_version.api_key_secret.secret_data
  line_channel_secret          = data.google_secret_manager_secret_version.line_channel_secret.secret_data
  line_channel_access_token    = data.google_secret_manager_secret_version.line_channel_access_token.secret_data
}
