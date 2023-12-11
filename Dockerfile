# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

ADD ./bot /app/bot
ADD .env /app/.env
ADD requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV NAME API_KEY
ENV NAME API_SECRET

CMD ["python", "-m", "bot"]