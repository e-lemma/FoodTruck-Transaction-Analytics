FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN mkdir data/

COPY extract_batch.py .
COPY transform_batch.py .
COPY load.py .
COPY pipeline.py .

CMD ["python3", "pipeline.py"]