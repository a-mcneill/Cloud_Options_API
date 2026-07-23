# Cloud Options API
A cloud-native microservice exposing European option pricing and Greeks via a FastAPI REST interface.
The service is built from a previously developed Python Black-Scholes pricing engine and deployed on Google Cloud Run to demonstrate practical cloud engineering, containerisation, and microservice deployment.

## Cloud Engineering
This project showcases:
- FastAPI microservice design
- Containerisation with Docker
- Deployment to Google Cloud Run
- Image management via Artifact Registry
- Stateless service design and autoscaling
- Public HTTPS API exposure
- GET/POST endpoint separation and request validation

## Project Overview
The API provides:
- European option pricing using the Black-Scholes model
- Full Greeks calculation (Delta, Gamma, Vega, Theta, Rho)
- JSON-based POST endpoints
- Simple GET endpoints for service status and usage guidance
- Auto-generated API documentation via `/docs` (FastAPI + Swagger)

The underlying pricing logic comes from a previously developed Python project, adapted into a cloud‑ready microservice.

## Features 
- **POST /price** — returns the Black‑Scholes option price  
- **POST /greeks** — returns Delta, Gamma, Vega, Theta, Rho  
- **GET /** — service status and endpoint listing  
- **GET /price** and **GET /greeks** — usage guidance  
- FastAPI + Pydantic request validation  
- Uvicorn ASGI server  
- Dockerised for reproducible builds  
- Cloud Run deployment with autoscaling

## Architecture
- `api.py` — FastAPI application exposing pricing and Greeks endpoints  
- `black_scholes.py` — pricing logic and Greeks implementation  
- `Dockerfile` — container build instructions using Python 3.11‑slim  
- `requirements.txt` — FastAPI, Uvicorn, SciPy 

---

## API Usage

### POST /price
Request:
```json
{
  "S": 100,
  "K": 100,
  "T": 1,
  "r": 0.05,
  "sigma": 0.2,
  "option_type": "call"
}
```

Response:
```json
{
  "Option Price": 10.450583572185565
}
```

### POST /greeks
Response:
```json
{
  "Delta": 3.095992775776506e-29,
  "Gamma": 1.7416699978607893e-29,
  "Vega": 3.4833399957215784e-28,
  "Theta": -9.960153399937793e-30,
  "Rho": 3.0423199051143127e-29
}
```

### Curl Example
```bash
curl -X POST \
  https://options-api-1096982697367.australia-southeast1.run.app/greeks \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "S": 100,
  "K": 1000,
  "T": 1,
  "r": 0.05,
  "sigma": 0.2,
  "option_type": "call"
}'
```

---

## Running Locally

Clone the repository and change into directory:
```bash
git clone https://github.com/a-mcneill/Cloud_Options_API.git

cd Cloud_Options_API
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the API:
```bash
uvicorn api:app --host 0.0.0.0 --port 8080
```

## Docker Instructions

Build the container image:
```bash
docker build -t options-api .
```

Tag the image for Artifact Registry:
```bash
docker tag options-api australia-southeast1-docker.pkg.dev/project-80240421-d4f7-4969-904/options-api/options-api
```

Push the image:
```bash
docker push australia-southeast1-docker.pkg.dev/project-80240421-d4f7-4969-904/options-api/options-api
```

## Deploying to Google Cloud Run
Deploy the pushed image:
```bash
gcloud run deploy options-api --image australia-southeast1-docker.pkg.dev/project-80240421-d4f7-4969-904/options-api/options-api --region australia-southeast1 --platform managed --allow-unauthenticated
```

### Cloud Run Endpoint
Cloud Run will provide a public HTTPS endpoint once deployment completes.
https://options-api-1096982697367.australia-southeast1.run.app/docs