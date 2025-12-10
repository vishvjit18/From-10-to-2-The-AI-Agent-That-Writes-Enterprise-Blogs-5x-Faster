<#
.SYNOPSIS
    Setup GCP resources and deploy the application to Cloud Run.
.DESCRIPTION
    This script helps with creating the Artifact Registry repo and deploying the app.
    YOU MUST UPDATE THE VARIABLES SECTION BEFORE RUNNING.
#>

# --- VARIABLES ---
$PROJECT_ID = "river-module-480616-t4"  # <--- REPLACE THIS
$REGION = "us-central1"
$REPO_NAME = "blog-writer-repo"
$SERVICE_NAME = "blog-writer-app"
# -----------------

# Validation check removed as user provided ID

# ensure gcloud is in path
$GCLOUD_PATH = "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin"
if (Test-Path $GCLOUD_PATH) {
    if ($env:Path -notlike "*$GCLOUD_PATH*") {
        Write-Host "Adding gcloud to Path for this session..."
        $env:Path = "$GCLOUD_PATH;$env:Path"
    }
} else {
    Write-Warning "Could not find gcloud at $GCLOUD_PATH. Please ensure it is in your PATH."
}

# Check for gcloud auth
Write-Host "Checking gcloud authentication..."
try {
    gcloud auth list --format="value(account)" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Not authenticated"
    }
} catch {
    Write-Error "Please run 'gcloud init' or 'gcloud auth login' to authenticate before running this script."
    exit 1
}


# 1. Enable APIs
Write-Host "Enabling required APIs..."
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 2. Create Artifact Registry Repository (if not exists)
Write-Host "Creating Artifact Registry repository '$REPO_NAME'..."
# Check if exists first to avoid error? or just try create and ignore specific error?
# We'll just run create and it might fail if exists, which is fine or we can verify.
gcloud artifacts repositories create $REPO_NAME `
    --repository-format=docker `
    --location=$REGION `
    --description="Blog writer images"
# Ignore error if it already exists

# 3. Build and Push Image
$IMAGE_URI = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME`:latest"
Write-Host "Building and pushing image to $IMAGE_URI..."
gcloud builds submit --tag $IMAGE_URI .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 4. Deploy to Cloud Run
# Read keys from config.yaml if available
$ConfigPath = Join-Path $PSScriptRoot "..\config.yaml"
$OpenRouterKey = "PLACEHOLDER"
$GoogleKey = "PLACEHOLDER"

if (Test-Path $ConfigPath) {
    Write-Host "Reading secrets from config.yaml..."
    $ConfigContent = Get-Content $ConfigPath -Raw
    if ($ConfigContent -match 'OPENROUTER_API_KEY:\s*"([^"]+)"') {
        $OpenRouterKey = $matches[1]
    }
    if ($ConfigContent -match 'GOOGLE_API_KEY:\s*"([^"]+)"') {
        $GoogleKey = $matches[1]
    }
}

gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_URI `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --port 8080 `
    --set-env-vars="OPENROUTER_API_KEY=$OpenRouterKey,GOOGLE_API_KEY=$GoogleKey"

Write-Host "Deployment complete. Please verify the service URL and update secrets via the Cloud Console or gcloud."
