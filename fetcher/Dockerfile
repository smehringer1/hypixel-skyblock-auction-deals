FROM python:3.8.5-alpine
WORKDIR /usr/src/fetcher
COPY . .
RUN pip install -r requirements.txt
CMD ["python","scheduler.py"]