from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load model and scaler
model = joblib.load('models/lightgbm_model.pkl')
scaler = joblib.load('models/scaler.pkl')


@app.route('/')
def home():
    return jsonify({
        'message': 'NIDS ML API is running',
        'endpoints': {
            '/predict': 'POST - Upload CSV for prediction',
            '/health': 'GET - Check API health'
        }
    })


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Accept CSV file upload
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        df = pd.read_csv(file)

        # Drop label columns if present
        drop_cols = [c for c in [' Label', 'binary_label'] if c in df.columns]
        df = df.drop(columns=drop_cols)

        # Scale and predict
        scaled = scaler.transform(df)
        predictions = model.predict(scaled)
        probabilities = model.predict_proba(scaled)

        results = []
        for i, pred in enumerate(predictions):
            results.append({
                'row': i + 1,
                'prediction': 'Attack' if pred == 1 else 'Benign',
                'confidence': round(float(max(probabilities[i])) * 100, 2)
            })

        summary = {
            'total_flows': len(predictions),
            'benign_count': int(sum(predictions == 0)),
            'attack_count': int(sum(predictions == 1)),
            'attack_percentage': round(float(sum(predictions == 1)) / len(predictions) * 100, 2)
        }

        return jsonify({
            'summary': summary,
            'results': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
