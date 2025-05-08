resource "google_cloud_run_service" "main" {
  name     = var.app_name
  location = var.location
  project  = var.project_id

  template {
    spec {
      containers {
        image = "${var.location}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repo_name}/${var.artifact_registry_image_name}:latest"
        resources {
          limits = {
            memory = "512Mi"
            cpu    = "1"
          }
        }
        ports {
          container_port = 8000
        }
        env {
          name  = "GOOGLE_API_KEY"
          value = var.google_ai_studio_api_key
        }
        env {
          name  = "LINE_CHANNEL_SECRET"
          value = var.line_channel_secret
        }
        env {
          name  = "LINE_CHANNEL_ACCESS_TOKEN"
          value = var.line_channel_access_token
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  location = google_cloud_run_service.main.location
  project  = google_cloud_run_service.main.project
  service  = google_cloud_run_service.main.name
  role     = "roles/run.invoker"
  member   = "allUsers" # 誰でもアクセス可能にする場合。制限したい場合は適宜変更。
}
