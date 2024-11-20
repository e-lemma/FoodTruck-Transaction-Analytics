FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY connect.py .
COPY charts.py .
COPY dashboard.py .
COPY config.toml .

CMD [ "streamlit", "run", "dashboard.py" ]