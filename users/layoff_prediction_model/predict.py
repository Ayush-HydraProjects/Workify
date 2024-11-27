import sys
import pandas as pd
import joblib
import json

def predict(data):
    # Load the model, scaler, and RFE
    model_filename = r'/Users/ayushparekh/Documents/IA:DS/Workify/Workify/users/layoff_prediction_model/RF_MODEL.pkl'
    scaler_filename = r'/Users/ayushparekh/Documents/IA:DS/Workify/Workify/users/layoff_prediction_model/scaler.pkl'
    rfe_filename = r'/Users/ayushparekh/Documents/IA:DS/Workify/Workify/users/layoff_prediction_model/RFE.pkl'

    loaded_model = joblib.load(model_filename)
    loaded_scaler = joblib.load(scaler_filename)
    loaded_rfe = joblib.load(rfe_filename)

    # Create a DataFrame from the input data
    sample_adjusted = pd.DataFrame([data])

    # Features used during training (including 'Age')
    training_feature_names = [
        'Age', 'EducationField', 'JobRole', 'Department', 'Industry',
        'Stage', 'Education', 'Funds_Raised(m)', 'PerformanceRating',
        'JobSatisfaction', 'JobInvolvement', 'YearsAtCompany',
        'YearsInCurrentRole', 'YearsWithCurrManager', 'MonthlyIncome',
        'NumCompaniesWorked', 'Gender'
    ]

    # Ensure sample_data includes all relevant features
    sample_adjusted = sample_adjusted[training_feature_names]

    # Transform the sample data using the scaler
    sample_adjusted_scaled = loaded_scaler.transform(sample_adjusted)

    # Transform the scaled data using RFE
    sample_adjusted_rfe = loaded_rfe.transform(sample_adjusted_scaled)

    # Predict the probability
    prob_adjusted = loaded_model.predict_proba(sample_adjusted_rfe)[:, 1]

    return prob_adjusted[0] * 100

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    # Convert input_data values to appropriate data types
    for key in input_data:
        try:
            input_data[key] = float(input_data[key])
        except ValueError:
            pass
    prediction = predict(input_data)
    print(prediction)
