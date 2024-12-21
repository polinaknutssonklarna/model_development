import pickle
import pandas as pd
import numpy as np
import json

from flask import Flask
from flask import request, jsonify

import logging

# Define the feature_engineering function
def feature_engineering(df):
    # Create target variable
    df['default'] = (df.amount_outstanding_21d > 0).astype(int)

    # Ensure loan_issue_date is datetime 
    
    df['loan_issue_date'] = pd.to_datetime(df['loan_issue_date'], errors='coerce')

    # Combine year and month for card expiration
    df['card_expiry_date'] = pd.to_datetime(
        df.apply(
            lambda row: f"{int(row['card_expiry_year'])}-{int(row['card_expiry_month']):02d}-01"
            if pd.notna(row['card_expiry_year']) and pd.notna(row['card_expiry_month'])
            else np.nan,
            axis=1
        ), 
        errors='coerce'
    )

    # Calculate the difference in months
    df['months_to_card_expiration'] = np.where(
        df['card_expiry_date'].notna() & df['loan_issue_date'].notna(),
        (df['card_expiry_date'].dt.year - df['loan_issue_date'].dt.year) * 12 +
        (df['card_expiry_date'].dt.month - df['loan_issue_date'].dt.month),
        np.nan
    )

    # Convert month_to_card_expiration to integer
    df['months_to_card_expiration'] = df['months_to_card_expiration'].fillna(-1).astype(int).replace(-1, np.nan)

    # Create a missingness flag for existing_klarna_debt
    df['existing_debt_missing'] = df['existing_klarna_debt'].isnull().astype(int)

    # Replace missing values for existing_klarna_debt with 0
    df['existing_klarna_debt'] = df['existing_klarna_debt'].fillna(0)

    # Create a missingness flag for card expiry date
    df['card_expiry_missing'] = df['card_expiry_month'].isnull().astype(int)

    # Loan_to_debt_ratio
    df['loan_to_debt_ratio'] = df['loan_amount'] / (df['existing_klarna_debt'] + df['loan_amount'])

    # New_exposure_7d_to_debt
    df['new_exposure_7d_to_debt'] = df['new_exposure_7d'] / (df['existing_klarna_debt'] + df['loan_amount'])

    # New_exposure_14d_to_debt
    df['new_exposure_14d_to_debt'] = df['new_exposure_14d'] / (df['existing_klarna_debt'] + df['loan_amount'])

    # Repayment to total debt
    df['repayment_1y_to_debt'] = (df['amount_repaid_1y'] / (df['existing_klarna_debt'] + df['loan_amount']))
    df['repayment_6m_to_debt'] = (df['amount_repaid_6m'] / (df['existing_klarna_debt'] + df['loan_amount']))
    df['repayment_3m_to_debt'] = (df['amount_repaid_3m'] / (df['existing_klarna_debt'] + df['loan_amount']))
    df['repayment_1m_to_debt'] = (df['amount_repaid_1m'] / (df['existing_klarna_debt'] + df['loan_amount']))
    df['repayment_14d_to_debt'] = (df['amount_repaid_14d'] / (df['existing_klarna_debt'] + df['loan_amount']))

    # Repayment_rate variations
    epsilon = 1e-5  # Small constant

    # Ratio of confirmed payments to active loans
    df['num_conf_payments_6m_to_num_loans'] = df['num_confirmed_payments_6m'] / (df['num_active_loans'] + epsilon)

    # Merchant categories
    top_n_categories = ['General Shoes & Clothing', 'Youthful Shoes & Clothing',
                         'Adult Shoes & Clothing', 'Event - Broker & Agencies',
                         'Travel - Accommodation & Resorts']

    # Merchant groups
    top_n_groups = ['Clothing & Shoes', 'Intangible products', 'Leisure, Sport & Hobby',
                     'Jewelry & Accessories', 'Home & Garden']

    # Reassign categories outside the top n and 'Unknown' to 'Other'
    df['merchant_category'] = df['merchant_category'].apply(
        lambda x: 'Other' if x not in top_n_categories or x == 'Unknown' else x
    )

    # Reassign groups outside the top n and 'Unknown' to 'Other'
    df['merchant_group'] = df['merchant_group'].apply(
        lambda x: 'Other' if x not in top_n_groups or x == 'Unknown' else x
    )

    return df




# Load the saved pipeline
model_file = 'final_model_pipeline.pkl'

with open(model_file, 'rb') as f_in:
    final_pipeline = pickle.load(f_in)

# Initialize Flask app
app = Flask('churn')

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def hello():
    return 'Test success! Use the /predict endpoint and POST a JSON object with customer data. ' 

@app.route('/predict', methods=['POST'])
def predict():    
    try:
        # Get JSON input 
        data = request.get_json()
        logging.info(f"Received customer data: {data}")

        # Check if input is valid
        if not data:
            return jsonify({'error': 'Invalid input: JSON is empty or missing'}), 400


        # Prepare data for prediction
        customer_df = pd.DataFrame([data])
        customer_df = feature_engineering(customer_df)
        logging.info(f"Converted data to DataFrame with shape: {customer_df.shape}")

        # Make predictions
        default_prob = float(final_pipeline.predict_proba(customer_df)[0, 1])
        #default = default_prob >= 0.5

        # Prepare response
        result = {
            'default_probability': round(default_prob, 3) #,
            #'default': bool(default)

            
        }

        logging.info(f"Prediction result: {result}")
        return jsonify(result)

    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')