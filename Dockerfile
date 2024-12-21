FROM python:3.9.20-slim


RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "final_model_pipeline.pkl", "./"]

EXPOSE 80

ENTRYPOINT ["python", "predict.py"]