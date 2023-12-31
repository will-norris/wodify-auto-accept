FROM python:3.8-alpine
RUN apk update
RUN apk add git
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "./src/app.py"]