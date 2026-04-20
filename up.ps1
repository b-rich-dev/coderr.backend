param([string]$message = "update")

git pull
git add .
git commit -m $message
git push
& "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.ps1" compute ssh eugen_birich@coderr-server --zone=europe-west3-c --command="cd ~/coderr.backend && git pull && docker compose up --build -d"


# .\up.ps1 "deine commit message"