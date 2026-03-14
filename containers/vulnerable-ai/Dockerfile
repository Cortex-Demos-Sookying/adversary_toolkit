FROM python:3.11-slim

WORKDIR /app

# Install dependencies (using inline pip for a cleaner single-file build)
RUN pip install flask langchain langchain-openai

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
