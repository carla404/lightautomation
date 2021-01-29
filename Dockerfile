# set base image (host OS)
FROM python:3.7-stretch

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY install-coap-client.sh .

# install dependencies
RUN pip3 install -r requirements.txt
RUN apt-get update -y && apt-get upgrade -y
RUN sh install-coap-client.sh

# copy the content of the local src directory to the working directory
COPY src/ .
COPY config.json .

# command to run on container start
CMD [ "python", "./main.py"]