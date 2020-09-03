# Config
# retrieve using `gcloud projects list`
GC_PROJECT=your-gcp-project-id
GC_PROJECT_NUMBER=your-gcp-project-number

# Grant the Cloud Run Admin role to the Cloud Build service account
gcloud projects add-iam-policy-binding $GC_PROJECT \
  --member "serviceAccount:$GC_PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role roles/run.admin

# Grant the IAM Service Account User role to the Cloud Build service account on the Cloud Run runtime service account
gcloud iam service-accounts add-iam-policy-binding \
  $GC_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --member="serviceAccount:$GC_PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"