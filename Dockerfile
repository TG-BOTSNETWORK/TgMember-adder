FROM python:3.8
WORKDIR /app
COPY . .
RUN 
CMD python3 -m adder
