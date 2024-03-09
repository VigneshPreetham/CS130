FROM python:3.8-slim

WORKDIR /app


COPY backend/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


COPY . /app

ENV FLASK_APP=backend/run.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
