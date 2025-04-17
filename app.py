from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the model from the saved location
model_path = r"d:/sem 6 project/bhaiya_project_files/DocHealth.Ai-StrokePrediction/stroke_model.pkl"
model = joblib.load(model_path)
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
        gender = {'Male': 1, 'Female': 0, 'Other': 2}
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
        input_data = np.array([[
            gender_val, age, hypertension, heart_disease, ever_married_val,
            work_type_val, residence_val, avg_glucose_level, bmi, smoking_status_val
        ]])

        # Predict
        prediction = model.predict(input_data)[0]

        return jsonify({
            "prediction": int(prediction),
            "message": "⚠️ High Stroke Risk" if prediction == 1 else "✅ Low Stroke Risk"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


print(model.predict([[1, 80, 1, 1, 1, 1, 1, 250.0, 45.0, 2]]))  # High risk example
