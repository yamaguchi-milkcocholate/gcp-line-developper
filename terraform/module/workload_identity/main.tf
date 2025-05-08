# github-actions用に作成したサービスアカウント
data "google_service_account" "main" {
  project    = var.project_id
  account_id = "github-actions-sa"
}

data "google_iam_workload_identity_pool" "main" {
  project                   = var.project_id
  workload_identity_pool_id = "github-pool"
}

resource "google_service_account_iam_member" "workload_identity_sa_iam" {
  service_account_id = data.google_service_account.main.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principal://iam.googleapis.com/${data.google_iam_workload_identity_pool.main.name}/subject/${var.github_repo_owner}/${var.github_repo_name}"
}
