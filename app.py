from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load the trained model and encoder
model = joblib.load('random_forest_model.pkl')
encoder = joblib.load('encoder_model.pkl')

# Define the expected columns based on the training data
expected_columns = ['distance', 'time'] + list(encoder.get_feature_names_out(['from', 'to', 'flightType', 'agency']))

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data from the request
        data = request.get_json(force=True)
        df = pd.DataFrame(data)

        # Preprocess the categorical columns
        categorical_cols = ['from', 'to', 'flightType', 'agency']
        categorical_features = df[categorical_cols]
        categorical_encoded = encoder.transform(categorical_features)
        categorical_df = pd.DataFrame(categorical_encoded, columns=encoder.get_feature_names_out(categorical_cols))

        # Concatenate the numerical features with the encoded categorical features
        numerical_features = df[['distance', 'time']]
        df_processed = pd.concat([numerical_features, categorical_df], axis=1)

        # Ensure all expected columns are present
        for col in expected_columns:
            if col not in df_processed.columns:
                df_processed[col] = 0

        # Reorder columns to match the training data
        df_processed = df_processed[expected_columns]

        # Make predictions
        prediction = model.predict(df_processed)

        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
