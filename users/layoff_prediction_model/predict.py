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

    # Get feature importance or coefficients (for explanation)
    feature_importance = loaded_model.feature_importances_

    # Create a dictionary to map features to their importance
    feature_explanation = {
        feature: importance
        for feature, importance in zip(training_feature_names, feature_importance)
    }

    # Actionable advice based on the data
    advice = []

    # Age: Career Progression and Experience
    if data['Age'] < 30:
        advice.append("As a younger professional, consider seeking mentorship to accelerate your growth and gain insights from more experienced colleagues.")
    elif data['Age'] > 50:
        advice.append("At a later stage in your career, it may be useful to focus on leadership skills or mentoring others to maintain job security.")

    # Education and Job Role Interrelation
    if data['Education'] < 3 and data['JobRole'] == 'Manager':
        advice.append("As a manager, pursuing further education or certifications could help boost your managerial skills and lead to better career growth.")
    elif data['Education'] < 3 and data['JobRole'] != 'Manager':
        advice.append("Consider pursuing higher education or certifications to specialize in your field, which could open up more opportunities.")

    # Industry and Job Satisfaction Interrelation
    if data['Industry'] == 'Technology' and data['JobSatisfaction'] < 3:
        advice.append("In the tech industry, if you're dissatisfied with your job, it could be due to rapid changes in technology. Upgrading your skills might help with job satisfaction.")
    elif data['Industry'] != 'Technology' and data['JobSatisfaction'] < 3:
        advice.append("In non-tech industries, job satisfaction may depend on work-life balance. It may be beneficial to discuss this with HR or your manager.")

    # Performance Rating and Job Satisfaction
    if data['PerformanceRating'] < 3 and data['JobSatisfaction'] < 3:
        advice.append("If both your performance and job satisfaction are low, it might be time to have a candid conversation with your manager about expectations and potential improvements.")
    elif data['PerformanceRating'] < 3:
        advice.append("Focusing on improving your performance, such as through additional training or taking on more responsibility, could lead to better performance reviews.")
    elif data['JobSatisfaction'] < 3:
        advice.append("Addressing job dissatisfaction by engaging with your manager or HR for support and setting achievable goals could improve your work-life balance.")

    # Monthly Income and Job Satisfaction Interrelation
    if data['MonthlyIncome'] < 5000 and data['JobSatisfaction'] < 3:
        advice.append("Consider discussing a salary review with your HR while also working on improving job satisfaction through clear communication and goal setting.")
    elif data['MonthlyIncome'] < 5000:
        advice.append("Exploring salary review opportunities or seeking roles with better compensation might be a good step if your current income doesn't align with your skills.")
    elif data['JobSatisfaction'] < 3:
        advice.append("If you're dissatisfied with your job, focusing on improving satisfaction could be beneficial, possibly through changing job responsibilities or work culture.")

    # YearsAtCompany and Performance Rating Interrelation
    if data['YearsAtCompany'] > 10 and data['PerformanceRating'] < 3:
        advice.append("If you've been with the company for a long time and performance is low, it might be time to reassess your goals and discuss future potential with your manager.")
    elif data['YearsAtCompany'] < 5 and data['PerformanceRating'] < 3:
        advice.append("A shorter tenure with low performance might require extra effort to prove your value. Consider additional responsibilities or training to improve your standing.")

    # Funds Raised and Career Stability
    if data['Funds_Raised(m)'] < 1000000:
        advice.append("If your company has raised limited funds, consider discussing long-term stability and potential career opportunities with your manager to ensure your future security.")

    # Gender: Gender-Specific Advice (if needed)
    if data['Gender'] == 'Female':
        advice.append("As a female employee, networking and mentorship within your company or industry could help in gaining leadership roles and advancing your career.")

    # Stage and Education Field Interrelation
    if data['Stage'] == 'Entry' and data['EducationField'] == 'Business':
        advice.append("As an entry-level professional in business, focusing on developing leadership skills and understanding the industry will set you up for better career advancement.")
    elif data['Stage'] == 'Mid-Level' and data['EducationField'] == 'Technology':
        advice.append("As a mid-level professional in tech, focusing on continuous learning and staying up to date with emerging technologies can enhance your value in the workplace.")

    # Department and Job Involvement Interrelation
    if data['Department'] == 'HR' and data['JobInvolvement'] < 3:
        advice.append("In HR, low job involvement may lead to burnout. It might be beneficial to take on different projects or responsibilities to feel more engaged.")
    elif data['Department'] == 'Sales' and data['JobInvolvement'] < 3:
        advice.append("In sales, low job involvement can impact performance. Finding ways to re-engage, such as setting clearer targets or exploring new sales techniques, might help.")

    # Return the predicted probability and the explanation/advice
    return prob_adjusted[0] * 100, feature_explanation, advice

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    # Convert input_data values to appropriate data types
    for key in input_data:
        try:
            input_data[key] = float(input_data[key])
        except ValueError:
            pass

    # Predict the layoff chance, feature importance, and advice
    prediction, feature_explanation, advice = predict(input_data)

    # Print the prediction and insights
    print(f"Layoff Chance: {prediction:.2f}%")
    print("Feature Importance Breakdown:")
    for feature, importance in feature_explanation.items():
        print(f"{feature}: {importance:.2f}")

    print("\nSuggestions to Improve Your Chances of Avoiding a Layoff:")
    for suggestion in advice:
        print(f"- {suggestion}")
