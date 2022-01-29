FROM python:3.9-slim
WORKDIR /
COPY . .
RUN pip3 install --no-cache-dir -q -r requirements.txt
CMD gunicorn --bind 0.0.0.0:$PORT run:app
