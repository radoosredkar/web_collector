# homes searcher
Finding apartments of intrest on various web sources

TODO:
- create docker compose for running all containers
- create build command that will:
		- run pip install -r requirements.txt
- create run command that will:
		- run python main.py
- extract parsers to separate files and module
- add cleaning of records, or better archieving
- add logging
- check wierd reporting of found new records for nepremicnine
- generalize both scrappers
- add somme commenting for choosen apartments

Docker commands:
```
sudo docker build -t wscr web_collector 
docker run -dit -p 5000:5000 wscr

sudo docker build -t wscr web_collector
docker run -dit --network wsc-network -p:5000:5000 --name wscr -v ~/software/python3/web_collector:/usr/code wscr 
```
