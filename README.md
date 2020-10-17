# homes searcher
Finding apartments of intrest on various web sources

TODO:
- extract parsers to separate files and moduke
- add cleaning of records, or better archieving
- add logging
- check wierd reporting of found new records for nepremicnine
- generalize both scrappers
- add somme commenting for choosen apartments

Docker commands:
```
sudo docker build -t wscr web_collector 
docker run -dit -p 5000:5000 wscr
```
