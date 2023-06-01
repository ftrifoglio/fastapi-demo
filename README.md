# Machine Learning microservice with FastAPI

Simple application with API endpoints to interact with machine learning models trained on the Titanic dataset.

There are 2 versions (`/v1` and `/v2`) each with two endpoints: `/predict` and `/score`.

`/v1` features a regularized logistic model. 

`/v2` features a random forest model.

`/predict` returns the predicted probability of survival.

`/score` returns some test set metrics of the model (ie ROC AUC, accuracy and recall).

## Usage

Build and launch the app with

```
docker-compose up
```

Send a POST request to the `/predict` endpoint

```
curl -X 'POST' \
  'http://localhost:8001/api/latest/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Age": 16,
  "SibSp": 1,
  "Parch": 2,
  "Sex": "male",
  "Embarked": "C",
  "Pclass": 1
}'
```

## Roadmap

- Add unit tests to `titanic_model` and `api_utils`
- Add logging (inspo: https://github.com/kurtispykes/car-evaluation-project)
- Make the image smaller
- Add CI/CD
