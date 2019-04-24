FROM python:3.7-alpine
WORKDIR /stellar-SMS

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev \
    postgresql-client \
    libpq \
    python-dev &&\
	pip install --upgrade pip &&\ 
    pip install -r requirements.txt &&\
    apk del .build-deps

# Copy over the rest of the project
COPY . /stellar-SMS
