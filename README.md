# homes searcher
Finding apartments of intrest on various web sources

TODO:
- deploy to some cloud infrastructire, preferablly AWS
- check redis sessions
- check wierd urls
- add docker builds only on certain tags
- extract parsers to separate files and module
- add cleaning of records, or better archieving
- check wierd reporting of found new records for nepremicnine
- generalize both scrappers
- add commenting for choosen apartments
- add filter changing (now it is fixed)
- add add to favorites and favorites filter
- add apartment size to the datamodel
- add enable and desable archieving
- add manual move to and from archive

Docker commands:
```
sudo docker build -t wscr web_collector 
docker run -dit -p 5000:5000 wscr

sudo docker build -t wscr web_collector
docker run -dit --network wsc-network -p:5000:5000 --name wscr -v ~/software/python3/web_collector:/usr/code wscr 
```
