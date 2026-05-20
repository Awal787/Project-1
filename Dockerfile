FROM python:3.11

WORKDIR /app

# ✅ copy only requirements first (better caching)
COPY requirements.txt .

# ✅ upgrade pip + install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy rest of the app
COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]