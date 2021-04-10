# homes searcher
Finding apartments of intrest on various web sources

TODO:
- check redis sessions
- add cleaning of records, or better archieving
- check wierd reporting of found new records for nepremicnine
- add filter changing (now it is fixed)
- add add to favorites and favorites filter
- add apartment size to the datamodel
- add enable and desable archieving (is it needed???)
- add manual move to and from archive (is it needed???)

IN PROGRESS
- Add status updating

DONE
- extract parsers to separate files and module
- generalize both scrappers
- deploy to some cloud infrastructire, preferablly AWS (gcp choosen)
- add docker builds only on selected tags (we are building only master branch instead)
- check wierd urls
- add commenting for choosen apartments

Docker commands:
```
sudo docker build -t wscr web_collector 
docker run -dit -p 5000:5000 wscr

sudo docker build -t wscr web_collector
docker run -dit --network wsc-network -p:5000:5000 --name wscr -v ~/software/python3/web_collector:/usr/code wscr 
```
