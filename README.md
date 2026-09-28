# SuperKart Sales Forecasting

## Overview
This project predicts SuperKart store sales using a machine learning model exposed through a Flask API and consumed by a Streamlit frontend.

## Repository Structure
```
GreatLearningSuperKart/
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── requirements.txt
│   ├── model/
│   │   └── superkart_model.joblib
│   └── tests/
│       └── test_app.py
├── frontend/
│   ├── streamlit_app.py
│   ├── requirements.txt
│   └── Dockerfile
├── data/
│   ├── train.csv
│   ├── test.csv
│   └── Batch_Data_SuperKart.csv
├── notebooks/
│   └── Full_Code_SuperKart_Model_Deployment_Notebook.ipynb
├── docker-compose.yml
└── README.md
```

## Quick Start (Docker Recommended)
1. Clone and enter the repository:
  ```bash
  git clone https://github.com/tagireddy/GreatLearningSuperKart.git
  cd GreatLearningSuperKart
  ```

2. Train or refresh the model artifact:
  ```bash
  docker compose run --rm -v ./data:/data backend python train_model.py
  ```

3. Build and run:
  ```bash
  docker compose up -d --build
  ```

4. Open the apps:
  - Frontend: http://localhost:8501
  - Backend API base: http://localhost:5001

## Local Run (Without Docker)
Run backend:
```bash
cd backend
pip install -r requirements.txt
python train_model.py
python app.py
```

Run frontend in another terminal:
```bash
cd frontend
pip install -r requirements.txt
BACKEND_URL=http://localhost:5001 streamlit run streamlit_app.py --server.port 8501
```

## API Endpoints
- `GET /health` - health status
- `GET /model-info` - expected model features and model path
- `POST /v1/predict` - single prediction
- `POST /v1/predictbatch` - batch prediction via uploaded CSV

## Testing
Run backend tests:
```bash
cd backend
python -m unittest discover -s tests -v
```

## Notes
- Docker maps backend container port `5000` to host port `5001` to avoid local macOS port conflicts.
- Frontend uses `BACKEND_URL` environment variable; default is `http://backend:5000` for container-to-container networking.