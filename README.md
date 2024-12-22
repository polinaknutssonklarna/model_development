# Deployment Repository for the Classification Case Study
The repository hosts a model that predicts the probability of default on a purchase made with the Pay Later payment method.

The model development repository can be found [in this folder](https://github.com/polinaknutssonklarna/model_development/tree/main/model_development).  


## Running the Model in a Local Environment
### 1. Build and run the Docker container locally

Execute the following commands to build and run the Docker container:

```
# Build Docker container
docker build -t credit_model_pk .

#Run container
docker run -it -p 80:80 credit_model_pk
```

### 2. Send a request locally

Send a request to the model using the following curl command:

```
curl -X POST -H "Content-Type: application/json" -d '{"loan_issue_date": "2023-09-22", "loan_amount": 9547, "amount_outstanding_14d": 7161, "amount_outstanding_21d": 7161, "card_expiry_month": 6.0, "card_expiry_year": 2027.0, "existing_klarna_debt": 0, "num_active_loans": 0, "days_since_first_loan": -1, "new_exposure_7d": 0, "new_exposure_14d": 0, "num_confirmed_payments_3m": 0, "num_confirmed_payments_6m": 0, "num_failed_payments_3m": 0, "num_failed_payments_6m": 0, "num_failed_payments_1y": 0, "amount_repaid_14d": 0, "amount_repaid_1m": 0, "amount_repaid_3m": 0, "amount_repaid_6m": 0, "amount_repaid_1y": 0, "merchant_group": "Leisure, Sport & Hobby", "merchant_category": "Concept Stores & Miscellaneous"}' http://localhost/predict
```

## Accessing the Model in a Cloud Environment
The model is deployed on AWS. To send a request to the AWS-hosted endpoint, use the following curl command:
```
curl -X POST -H "Content-Type: application/json" -d '{"loan_issue_date": "2023-09-22", "loan_amount": 9547, "amount_outstanding_14d": 7161, "amount_outstanding_21d": 7161, "card_expiry_month": 6.0, "card_expiry_year": 2027.0, "existing_klarna_debt": 0, "num_active_loans": 0, "days_since_first_loan": -1, "new_exposure_7d": 0, "new_exposure_14d": 0, "num_confirmed_payments_3m": 0, "num_confirmed_payments_6m": 0, "num_failed_payments_3m": 0, "num_failed_payments_6m": 0, "num_failed_payments_1y": 0, "amount_repaid_14d": 0, "amount_repaid_1m": 0, "amount_repaid_3m": 0, "amount_repaid_6m": 0, "amount_repaid_1y": 0, "merchant_group": "Leisure, Sport & Hobby", "merchant_category": "Concept Stores & Miscellaneous"}'  http://polina-predict-appv2.eu-west-1.elasticbeanstalk.com/predict
```


## Features
The list of features
```
loan_amount
TBC
```