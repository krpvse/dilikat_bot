FROM python:3.10.0

WORKDIR /bot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY .env .
COPY . .

CMD python3 main.py
