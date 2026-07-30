# ML-Powered Network Intrusion Detection System (NIDS)

A machine learning system that detects malicious network traffic — including DDoS, port scan, and brute-force attacks — trained on the CICIDS2017 dataset and served through a Flask REST API with an interactive dashboard. Fully containerized with Docker and tested automatically on every push via GitHub Actions CI/CD.

![CI/CD Pipeline](https://github.com/yepurirevanth06/network-intrusion-detection-ml/actions/workflows/ci-cd.yml/badge.svg)

## Results

| Model | Accuracy | F1-Score |
|---|---|---|
| **LightGBM** | **99.98%** | **99.98%** |
| Random Forest | 99.96% | 99.94% |

Trained and evaluated on **692,703 labeled network flows** with **78 traffic features** from the [CICIDS2017 dataset](https://www.unb.ca/cic/datasets/ids-2017.html).

## Features

- **Data pipeline** — cleaning and preprocessing of 692K+ flows, including handling of 1,000+ missing and 1,500+ infinite values, with feature scaling via StandardScaler
- **ML models** — Random Forest and LightGBM classifiers with confusion matrix and feature importance analysis (see `eda.ipynb`)
- **REST API** — Flask endpoints for health checks (`/health`) and batch prediction (`/predict`) from uploaded CSV files
- **Interactive dashboard** — dark-themed web UI with CSV upload, per-flow attack/benign classification, confidence scores, and summary statistics
- **Docker** — single-command containerized deployment
- **CI/CD** — GitHub Actions pipeline running an 8-test pytest suite (model integrity + API endpoints) and an automated Docker build with a health-check smoke test on every push

## Project Structure

```
├── app/
│   ├── app.py              # Flask API + dashboard routes
│   └── templates/          # Dashboard frontend
├── models/
│   ├── lightgbm_model.pkl  # Trained LightGBM classifier
│   ├── random_forest_model.pkl
│   └── scaler.pkl          # Fitted StandardScaler
├── tests/
│   ├── test_model.py       # Model + scaler integrity tests
│   └── test_api.py         # API endpoint tests
├── .github/workflows/
│   └── ci-cd.yml           # CI/CD pipeline
├── eda.ipynb               # EDA, preprocessing, model training
├── Dockerfile
├── requirements.txt
└── sample_test.csv         # Sample input for the API
```

## Quick Start

### Run with Docker (recommended)

```bash
docker build -t nids-app .
docker run -p 5001:5001 nids-app
```

Open **http://localhost:5001** for the dashboard.

### Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

### Run the tests

```bash
python -m pytest tests/ -v
```

## API Usage

**Health check**

```bash
curl http://localhost:5001/health
```

**Predict from a CSV of network flows**

```bash
curl -X POST http://localhost:5001/predict \
  -F "file=@sample_test.csv"
```

Returns JSON with per-flow predictions (`Attack`/`Benign`), confidence scores, and a summary (total flows, benign count, attack count).

## Tech Stack

Python · scikit-learn · LightGBM · pandas · NumPy · Flask · pytest · Docker · GitHub Actions

## Roadmap

- [ ] Deploy to AWS EC2 with automated CD
- [ ] Multi-class attack-type classification
- [ ] Live traffic capture integration

## Author

**Revanth Yepuri** — [LinkedIn](https://linkedin.com/in/revanth-yepuri) · [GitHub](https://github.com/yepurirevanth06)