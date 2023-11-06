FROM python:3.10-slim-buster

COPY . /home/oncall/metrics/

RUN pip install wheel
RUN pip install -r /home/oncall/metrics/requirements.txt

EXPOSE 8090

CMD ["python /home/oncall/metrics/metrics.py"]
