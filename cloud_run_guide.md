# Deploying to Google Cloud Run

**Google Cloud Run** is a fully managed serverless platform that is ideal for Python containers.

## 💰 Cost
Cloud Run has a generous **Free Tier**:
- **First 2 million requests/month**: Free.
- **First 180,000 vCPU-seconds/month**: Free.
- **First 360,000 GB-seconds/month**: Free.

For this application, it will likely cost **$0.00/month** unless you have massive traffic. If you exceed the free tier, you only pay for the exact time your code runs (measured in 100ms increments).

## 🚀 Deployment Steps

### Prerequisites
1.  [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed (`gcloud`).
2.  A Google Cloud Project.

### Step 1: Initialize
Login and set your project ID:
```bash
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```

### Step 2: Enable Services
Enable Cloud Run and Container Registry:
```bash
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
```

### Step 3: Deploy
Run the following single command to build and deploy. Replace the API Keys with your actual values.

```bash
gcloud run deploy mxv-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_gemini_key,PINECONE_API_KEY=your_pinecone_key"
```

### Step 4: Access
The command will output a URL (e.g., `https://mxv-chatbot-205276036567.us-central1.run.app`). Open this URL to use your app.

## ⚠️ Important Notes
- **Persistence**: Like Vercel, Cloud Run containers are ephemeral. If the service scales down to zero or restarts (which happens frequently), **chat history in `mxv.db` will be reset**. The sales data will persist because it is baked into the container image.
- **Rate Limiting**: Your rate limiter works per container instance.
