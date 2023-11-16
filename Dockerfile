FROM python:3.11.0

WORKDIR /bot

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY .bot-env ./

COPY . /.

CMD python main.py
