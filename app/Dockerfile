FROM python:3.6
EXPOSE 5000
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install pendulum service_identity
RUN pip install PyMySQL
RUN pip install -r requirements.txt
CMD python run.py
