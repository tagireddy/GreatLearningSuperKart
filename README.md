# SuperKart Sales Forecasting Project

## Overview
The SuperKart Sales Forecasting project aims to develop a robust machine learning solution for predicting sales revenue across various retail outlets of SuperKart, a retail chain operating supermarkets and food marts. The project encompasses data preprocessing, model training, evaluation, and deployment using a Flask backend and a Streamlit frontend.

## Project Structure
```
superkart-forecasting
├── backend                # Backend application for serving predictions
│   ├── app.py            # Main entry point for the Flask application
│   ├── model             # Directory containing the serialized model
│   │   └── superkart_model.joblib
│   ├── requirements.txt   # Python dependencies for the backend
│   └── Dockerfile        # Dockerfile for building the backend image
├── frontend               # Frontend application for user interaction
│   ├── streamlit_app.py   # Main entry point for the Streamlit application
│   ├── requirements.txt    # Python dependencies for the frontend
│   └── Dockerfile        # Dockerfile for building the frontend image
├── data                   # Datasets used for training and testing
│   ├── train.csv         # Training dataset
│   ├── test.csv          # Test dataset
│   └── Batch_Data_SuperKart.csv  # Batch dataset for bulk predictions
├── notebooks              # Jupyter notebooks for development and documentation
│   └── Full_Code_SuperKart_Model_Deployment_Notebook.ipynb
├── .devcontainer          # Configuration for development container
│   └── devcontainer.json
├── .github                # GitHub workflows for CI/CD
│   └── workflows
│       └── ci.yml
├── docker-compose.yml     # Docker Compose file for multi-container setup
├── .gitignore             # Files and directories to ignore in Git
└── README.md              # Project documentation
```

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd superkart-forecasting
   ```

2. **Install Dependencies**
   - For the backend:
     ```bash
     cd backend
     pip install -r requirements.txt
     ```
   - For the frontend:
     ```bash
     cd ../frontend
     pip install -r requirements.txt
     ```

3. **Run the Application**
   - Start the backend server:
     ```bash
     cd backend
     python app.py
     ```
   - Start the frontend application:
     ```bash
     cd ../frontend
     streamlit run streamlit_app.py
     ```

4. **Docker Setup**
   - Build and run the Docker containers:
     ```bash
     docker-compose up --build
     ```

## Usage
- Access the frontend application through the provided URL after starting the Streamlit app.
- Use the interface to input product details and receive sales predictions.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.