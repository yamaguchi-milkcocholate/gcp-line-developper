variable "project_id" {
  description = "Google Cloud プロジェクト ID"
  type        = string
}

variable "location" {
  description = "Google Cloud リージョン"
  type        = string
}

variable "app_name" {
  description = "アプリケーション名"
  type        = string
}

variable "artifact_registry_repo_name" {
  description = "Artifact Registry リポジトリ名"
  type        = string
}

variable "artifact_registry_image_name" {
  description = "Artifact Registry イメージ名"
  type        = string
}

variable "google_ai_studio_api_key" {
  description = "Google AI Studio API キー"
  type        = string
  sensitive   = true
}

variable "line_channel_secret" {
  description = "LINE チャネルシークレット"
  type        = string
  sensitive   = true
}

variable "line_channel_access_token" {
  description = "LINE チャネルアクセストークン"
  type        = string
  sensitive   = true
}
