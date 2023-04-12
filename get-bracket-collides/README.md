# Seeding

This code is meant to run on Google Cloud Functions.

## Environment variables

For local tests they need to be accessible with `os.environ.get`. For Cloud Functions environnements, they can be listed directly in the GCP console.

- `GOOGLE_APPLICATION_CREDENTIALS` : Path to your GCP JSON key to access the firestore base when running locally

## Testing locally

`python -c "from main import main; main()"`

## Deploy to GCP

`gcloud functions deploy get-bracket-collides --region europe-west1`
