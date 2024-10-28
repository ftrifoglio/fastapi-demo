# Machine Learning Microservice with FastAPI

This application serves machine learning models trained on the Titanic dataset, allowing API-based predictions and model evaluation.

## API Overview

There are two versions of the API (`/v1` and `/v2`), each offering two endpoints: `/predict` and `/score`.

- **`/v1`**: Utilizes a regularized logistic regression model.
- **`/v2`**: Utilizes a random forest model.
- **`/predict`**: Returns the predicted probability of passenger survival.
- **`/score`**: Provides model metrics on a test set (ROC AUC, accuracy, and recall).

## Deployment

The app is deployed with continuous integration to AWS ECS using a Terraform template. GitHub Actions handles automated deployments on changes to the main branch.

## Local Usage

To run the app locally using Docker:

```bash
$ git clone https://github.com/ftrifoglio/fastapi-demo.git
$ cd fastapi-demo
$ docker-compose up
```

## Roadmap

- Add unit tests to `titanic_model` and `api_utils`