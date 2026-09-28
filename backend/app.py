from flask import Flask, request, jsonify
import joblib
import pandas as pd
from pathlib import Path

app = Flask(__name__)

EXPECTED_FEATURES = [
    'Product_Weight',
    'Product_Sugar_Content',
    'Product_Allocated_Area',
    'Product_MRP',
    'Store_Size',
    'Store_Location_City_Type',
    'Store_Type',
    'Product_Id_char',
    'Store_Age_Years',
    'Product_Type_Category',
]


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()

    if 'Product_Id_char' not in prepared.columns and 'Product_Id' in prepared.columns:
        prepared['Product_Id_char'] = prepared['Product_Id'].astype(str).str.extract(r'([A-Za-z]+)', expand=False)

    if 'Product_Type_Category' not in prepared.columns and 'Product_Type' in prepared.columns:
        prepared['Product_Type_Category'] = prepared['Product_Type']

    if 'Store_Age_Years' not in prepared.columns and 'Store_Establishment_Year' in prepared.columns:
        current_year = pd.Timestamp.now().year
        prepared['Store_Age_Years'] = current_year - pd.to_numeric(
            prepared['Store_Establishment_Year'], errors='coerce'
        )

    missing = [col for col in EXPECTED_FEATURES if col not in prepared.columns]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    return prepared[EXPECTED_FEATURES]


model_path = Path('model/superkart_model.joblib')
model = joblib.load(model_path)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
    })


@app.route('/model-info', methods=['GET'])
def model_info():
    return jsonify({
        'model_path': str(model_path),
        'expected_features': EXPECTED_FEATURES,
    })

@app.route('/v1/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    try:
        input_df = pd.DataFrame([data])
        features = prepare_features(input_df)
        prediction = model.predict(features)
        return jsonify({'sales': float(prediction[0])})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 400

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    file = request.files['file']

    try:
        batch_data = pd.read_csv(file)
        features = prepare_features(batch_data)
        predictions = model.predict(features)
        return jsonify(predictions.tolist())
    except Exception as exc:
        return jsonify({'error': str(exc)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)