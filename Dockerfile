# set base image (host OS)
FROM python:3.8

# set the working directory in the container
RUN apt-get update && apt-get install -y vim
RUN mkdir /usr/src/web_collector
WORKDIR /usr/src/web_collector

RUN /usr/local/bin/python -m pip install --upgrade pip

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r /usr/src/web_collector/requirements.txt

# copy the content of the local src/web_collector directory to the working directory
#COPY . .

EXPOSE 5000

RUN echo "pip install -r /usr/src/web_collector/requirements.txt" > /usr/bin/build
RUN echo "python /usr/src/web_collector/main.py" > /usr/bin/run
RUN chmod +x /usr/bin/build
RUN chmod +x /usr/bin/run

# command to run on container start
#CMD [ "python", "/usr/src/web_collector/main.py" ] 
CMD [ "flask", "run", "--host=0.0.0.0" ] 
