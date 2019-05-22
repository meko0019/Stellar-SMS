FROM python:3.7-alpine

WORKDIR /stellar-SMS

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .
RUN apk update && \
	apk add --no-cache \
	    build-base \
	    python3-dev \
	    curl \
	    git \
	    gcc \
	    libstdc++ \
	    musl-dev \
	    libffi-dev \
	    postgresql-dev \
	    postgresql-client &&\
	pip install --upgrade pip &&\ 
    pip install -r requirements.txt 

# Copy over the rest of the project
COPY . /stellar-SMS
