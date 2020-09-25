FROM python:3.8.5-alpine
WORKDIR /usr/src/flaskapp
COPY . .
RUN pip install -r requirements.txt
CMD ["python","app.py"]