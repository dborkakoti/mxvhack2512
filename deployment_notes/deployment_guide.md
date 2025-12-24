# Deploying to Vercel

Follow these steps to deploy your Chatbot to Vercel.

## Prerequisites
- A [Vercel Account](https://vercel.com/signup).
- [Vercel CLI](https://vercel.com/docs/cli) installed (`npm i -g vercel`) OR simply use the Vercel Dashboard with your GitHub repository.

## Step 1: Push to GitHub
Ensure your latest code (including `vercel.json` and `requirements.txt`) is pushed to your GitHub repository.

## Step 2: Import Project in Vercel
1.  Go to the [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** -> **"Project"**.
3.  Import your GitHub repository `mxvhack2512`.

## Step 3: Configure Environment Variables
**Crucial Step**: Vercel needs your API keys to run.
In the "Configure Project" screen, expand **"Environment Variables"** and add:

| Key | Value |
| :--- | :--- |
| `GOOGLE_API_KEY` | *Your Gemini API Key* |
| `PINECONE_API_KEY` | *Your Pinecone API Key* |
| `GEMINI_API_KEY` | *(Optional, if you use this var name)* |

## Step 4: Deploy
Click **"Deploy"**. Vercel will:
1.  Detect `requirements.txt` and install Python dependencies.
2.  Detect `vercel.json` and configure the routing.
3.  Deploy your app to `https://mxvhack2512.vercel.app` (or similar).

## Important Notes on Data
- **Sales Data**: The `mxv.db` file included in your repo will be used. It contains the sales data you imported.
- **Chat History**: Since Vercel is "serverless", the file system is read-only. Chat history will **NOT be saved** permanently. If you restart the app or between different user sessions, the history in `mxv.db` will not persist.
- **Rate Limiting**: Your rate limiter works per server instance.

## Troubleshooting
- **Logs**: If the app fails, check the "Logs" tab in display Vercel Dashboard.
- **Timeouts**: If Gemini takes >10 seconds, the request might time out on the free tier.
