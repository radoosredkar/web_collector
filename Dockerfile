# set base image (host OS)
FROM python:3.8

# set the working directory in the container
RUN apt-get update && apt-get install -y vim
RUN mkdir /usr/code
WORKDIR /usr/code

RUN /usr/local/bin/python -m pip install --upgrade pip

# copy the dependencies file to the working directory
#COPY requirements.txt .

# install dependencies
#RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
#COPY . .

EXPOSE 5000

# command to run on container start
#CMD [ "python", "./main.py" ] 
