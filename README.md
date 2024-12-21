<!--
This document provides instructions for creating an application using the UI with Docker and a provided sample application. 
Steps include:
1. Creating the environment.
2. Selecting disk version 3.
3. Ensuring MDS v1 is disabled (default setting in UI).
4. Waiting for the app to start and display the default app.
5. Running three commands, replacing placeholders with your app name and environment.
-->





eb init -p docker predict-app-v2 -r eu-west-1
eb use Predict-app-v2-env
eb deploy


# Build Docker container
docker build -t credit_model_pk .

# Run container
docker run -it -p 80:80 credit_model_pk

# Deploy on AWS
eb use Predict-app-v2-env
eb deploy


# make curl call using terminal
# AWS
# curl -X POST -H "Content-Type: application/json" -d '{"person_age":27,"person_income":47900,"person_home_ownership":"OWN","person_emp_length":1.0,"loan_intent":"VENTURE","loan_grade":"C","loan_amnt":7500,"loan_int_rate":13.47,"loan_percent_income":0.16,"cb_person_default_on_file":"N","cb_person_cred_hist_length":6}' http://polina-predict-appv2.eu-west-1.elasticbeanstalk.com/predict

# local
# curl -X POST -H "Content-Type: application/json" -d '{"person_age":27,"person_income":47900,"person_home_ownership":"OWN","person_emp_length":1.0,"loan_intent":"VENTURE","loan_grade":"C","loan_amnt":7500,"loan_int_rate":13.47,"loan_percent_income":0.16,"cb_person_default_on_file":"N","cb_person_cred_hist_length":6}' http://localhost/predict


-----------------------

## Running the Model Locally
1. Build and run the Docker container locally

Execute the following commands to build and run the Docker container:

```
### Build Docker container
docker build -t credit_model_pk .

### Run container
docker run -it -p 80:80 credit_model_pk
```

2. Send a request locally

Send a request to the model using the following curl command:

```
curl -X POST -H "Content-Type: application/json" -d '{"loan_issue_date": "2023-09-22", "loan_amount": 9547, "amount_outstanding_14d": 7161, "amount_outstanding_21d": 7161, "card_expiry_month": 6.0, "card_expiry_year": 2027.0, "existing_klarna_debt": 0, "num_active_loans": 0, "days_since_first_loan": -1, "new_exposure_7d": 0, "new_exposure_14d": 0, "num_confirmed_payments_3m": 0, "num_confirmed_payments_6m": 0, "num_failed_payments_3m": 0, "num_failed_payments_6m": 0, "num_failed_payments_1y": 0, "amount_repaid_14d": 0, "amount_repaid_1m": 0, "amount_repaid_3m": 0, "amount_repaid_6m": 0, "amount_repaid_1y": 0, "merchant_group": "Leisure, Sport & Hobby", "merchant_category": "Concept Stores & Miscellaneous"}' http://localhost/predict
```

## Sending Requests to the AWS
The model is also deployed on AWS. To send a request to the AWS-hosted endpoint, use the following curl command:
```
curl -X POST -H "Content-Type: application/json" -d '{"loan_issue_date": "2023-09-22", "loan_amount": 9547, "amount_outstanding_14d": 7161, "amount_outstanding_21d": 7161, "card_expiry_month": 6.0, "card_expiry_year": 2027.0, "existing_klarna_debt": 0, "num_active_loans": 0, "days_since_first_loan": -1, "new_exposure_7d": 0, "new_exposure_14d": 0, "num_confirmed_payments_3m": 0, "num_confirmed_payments_6m": 0, "num_failed_payments_3m": 0, "num_failed_payments_6m": 0, "num_failed_payments_1y": 0, "amount_repaid_14d": 0, "amount_repaid_1m": 0, "amount_repaid_3m": 0, "amount_repaid_6m": 0, "amount_repaid_1y": 0, "merchant_group": "Leisure, Sport & Hobby", "merchant_category": "Concept Stores & Miscellaneous"}'  http://polina-predict-appv2.eu-west-1.elasticbeanstalk.com/predict
```



curl -X POST -H "Content-Type: application/json" -d '{"loan_id": "45e3d15cb313d767470722e952e14313", "loan_issue_date": "2023-09-22", "loan_amount": 9547, "amount_outstanding_14d": 7161, "amount_outstanding_21d": 7161, "card_expiry_month": 6.0, "card_expiry_year": 2027.0, "existing_klarna_debt": 0, "num_active_loans": 0, "days_since_first_loan": -1, "new_exposure_7d": 0, "new_exposure_14d": 0, "num_confirmed_payments_3m": 0, "num_confirmed_payments_6m": 0, "num_failed_payments_3m": 0, "num_failed_payments_6m": 0, "num_failed_payments_1y": 0, "amount_repaid_14d": 0, "amount_repaid_1m": 0, "amount_repaid_3m": 0, "amount_repaid_6m": 0, "amount_repaid_1y": 0, "merchant_group": "Leisure, Sport & Hobby", "merchant_category": "Concept Stores & Miscellaneous"}' http://localhost/predict

## Call the model from AWS
# curl -X POST -H "Content-Type: application/json" -d '{"loan_id": "45e3d15cb313d767470722e952e14313", "loan_issue_date": "2023-09-22", "loan_amount": 9547, "amount_outstanding_14d": 7161, "amount_outstanding_21d": 7161, "card_expiry_month": 6.0, "card_expiry_year": 2027.0, "existing_klarna_debt": 0, "num_active_loans": 0, "days_since_first_loan": -1, "new_exposure_7d": 0, "new_exposure_14d": 0, "num_confirmed_payments_3m": 0, "num_confirmed_payments_6m": 0, "num_failed_payments_3m": 0, "num_failed_payments_6m": 0, "num_failed_payments_1y": 0, "amount_repaid_14d": 0, "amount_repaid_1m": 0, "amount_repaid_3m": 0, "amount_repaid_6m": 0, "amount_repaid_1y": 0, "merchant_group": "Leisure, Sport & Hobby", "merchant_category": "Concept Stores & Miscellaneous"}'  http://polina-predict-appv2.eu-west-1.elasticbeanstalk.com/predict



