FROM python:3.9

WORKDIR /app

COPY requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-${RUN_MODE}.txt

# python setup.py develop

COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

CMD ["python", "main.py"]