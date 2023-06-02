# Machine Learning microservice with FastAPI

App to interact with machine learning models trained on the Titanic dataset.

There are 2 versions (`/v1` and `/v2`) each with two API endpoints: `/predict` and `/score`.

`/v1` features a regularized logistic model. `/v2` features a random forest model. `/predict` returns the predicted probability of survival. `/score` returns some test set metrics of the model (ie ROC AUC, accuracy and recall).

## Live demo

The app is currently (and hopefully) live on AWS ECS (Amazon Elastic Container Service)

http://fastapi-demo-nlb-ec2-cc72dbfaa6e8866d.elb.eu-west-1.amazonaws.com

## Usage

Build and spin up the app locally using Docker

```
$ git clone https://github.com/fedassembly/fastapi-demo.git
$ cd fastapi-demo
$ make venv  # works on MacOS only
$ docker-compose up
```

## Roadmap

- Add unit tests to `titanic_model` and `api_utils`
- Add CI/CD
