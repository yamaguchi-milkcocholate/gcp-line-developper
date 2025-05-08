output "account_id" {
  value = data.google_service_account.main.account_id
}

output "account_email" {
  value = data.google_service_account.main.email
}
