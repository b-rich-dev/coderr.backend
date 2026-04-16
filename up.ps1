param([string]$message = "update")

git pull
git add .
git commit -m $message
git push
gcloud compute ssh eugen_birich@coderr-server --zone=europe-west3-c --command="cd ~/coderr.backend && git pull && docker compose up --build -d"
