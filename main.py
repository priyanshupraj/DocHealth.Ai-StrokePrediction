import joblib
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})

# Load the model from the saved location
model = joblib.load("stroke_model.pkl")
print("Model loaded successfully:", type(model))

# Home route
@app.route('/', methods=['GET'])
def home():
    return 'Stroke Prediction API is running locally!'

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Encoding dictionaries (must match your training encodings!)
        gender = {'Male': 1, 'Female': 0}
        ever_married = {'No': 0, 'Yes': 1}
        work_type = {'children': 0, 'Govt_job': 1, 'Never_worked': 2, 'Private': 3, 'Self-employed': 4}
        residence_type = {'Rural': 0, 'Urban': 1}
        smoking_status = {'formerly smoked': 0, 'never smoked': 1, 'smokes': 2, 'Unknown': 3}

        # Extract and encode inputs
        gender_val = gender[data["gender"]]
        age = float(data["age"])
        hypertension = int(data["hypertension"])
        heart_disease = int(data["heart_disease"])
        ever_married_val = ever_married[data["ever_married"]]
        work_type_val = work_type[data["work_type"]]
        residence_val = residence_type[data["Residence_type"]]
        avg_glucose_level = float(data["avg_glucose_level"])
        bmi = float(data["bmi"])
        smoking_status_val = smoking_status[data["smoking_status"]]

        # Create input array for model
        input_data = pd.DataFrame([{
            "gender": gender_val,
            "age": age,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "ever_married": ever_married_val,
            "work_type": work_type_val,
            "Residence_type": residence_val,
            "avg_glucose_level": avg_glucose_level,
            "bmi": bmi,
            "smoking_status": smoking_status_val
        }])

        # Predict
        prediction = model.predict(input_data)[0]

        return jsonify({
            "prediction": int(prediction),
            "message": "⚠️ High Stroke Risk" if prediction == 1 else "✅ Low Stroke Risk"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Run locally
if __name__ == '__main__':
    app.run(debug=True)
    