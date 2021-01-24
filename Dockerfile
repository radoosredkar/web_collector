# set base image (host OS)
FROM python:3.8

# set the working directory in the container
RUN apt-get update && apt-get install -y vim
RUN mkdir /usr/src/web_collector
RUN mkdir /var/log/web_collector
WORKDIR /usr/src/web_collector

RUN /usr/local/bin/python -m pip install --upgrade pip
# Install datadog
# For successful build we have to disable datadog on docker hub
#RUN DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<ADD KEY> DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
#RUN pip install datadog
EXPOSE 5001
#RUN service datadog-agent restart

# copy the dependencies file to the working directory
COPY web_collector/requirements.txt .

# install dependencies
RUN pip install -r /usr/src/web_collector/requirements.txt

# copy the content of the local src/web_collector directory to the working directory
#COPY . .

EXPOSE 5000

RUN echo "pip install -r /usr/src/web_collector/requirements.txt" > /usr/bin/build
RUN echo "python /usr/src/web_collector/main.py" > /usr/bin/run
#RUN "datadog-agent run"
RUN chmod +x /usr/bin/build
RUN chmod +x /usr/bin/run

# command to run on container start
#CMD [ "python", "/usr/src/web_collector/main.py" ] 
#CMD [ "datadog-agent", "run"] 
CMD [ "flask", "run", "--host=0.0.0.0" ] 
