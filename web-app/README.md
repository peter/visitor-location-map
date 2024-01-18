# Visitor Location Map - Web App

This is the web app that displays visitor locations. It was created using Vite, React, TypeScript, and Google Maps.

## Developer Setup

To run the web app you need to have the REST API running.

```sh
# Install dependencies
npm install

# Copy the env file and set VITE_GOOGLE_MAPS_API_KEY
cp .env.example .env

# Start Development Server
npm run dev

# Open a browser
open http://localhost:5173
```

## Deployment

The app is deployed using [Vercel](https://vercel.com) to [visitor-location-map.vercel.app](https://visitor-location-map.vercel.app):

```sh
# Build/test locally:
npm run build
npm run preview

# Install Vercel CLI and set up Vercel account
npm i -g vercel

# Preview/stage deploy
vercel

# Production deploy
vercel --prod
```
