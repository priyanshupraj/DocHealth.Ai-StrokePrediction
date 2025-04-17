from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib

# Load data
df = pd.read_csv("d:/sem 6 project/bhaiya_project_files/DocHealth.Ai-StrokePrediction/healthcare-dataset-stroke-data.csv")
df.drop("id", axis=1, inplace=True)
df["bmi"] = df["bmi"].fillna(df["bmi"].median())

# Encode categorical features
categorical = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]
for col in categorical:
    df[col] = LabelEncoder().fit_transform(df[col])

# Features and target
X = df.drop("stroke", axis=1)
y = df["stroke"]

# 💡 Apply SMOTE to handle imbalance
sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X, y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, zero_division=0))

# Save model
joblib.dump(model, "stroke_model.pkl")
print ("model saved as stroke_model.pkl")