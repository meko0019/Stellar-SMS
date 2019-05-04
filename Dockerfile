FROM python:3.7

WORKDIR /stellar-SMS

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

RUN apt-get update && apt-get install -y postgresql postgresql-client &&\
	pip install --upgrade pip &&\ 
    pip install -r requirements.txt 

# Copy over the rest of the project
COPY . /stellar-SMS
