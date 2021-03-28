# set base image (host OS)
FROM python:3.7-stretch

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY install-coap-client.sh .

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install libbluetooth-dev -y
RUN apt-get install pkg-config -y
RUN apt-get install libglib2.0-dev -y
RUN apt-get install libboost-all-dev -y
RUN pip3 install -r requirements.txt
RUN sh install-coap-client.sh

# copy the content of the local src directory to the working directory
COPY src/ .
COPY config.json .

# command to run on container start
CMD [ "python", "./main.py"]