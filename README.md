# homes searcher
Finding apartments of intrest on various web sources

TODO:
- Is it safe to injec secrets to env on build?
- check redis sessions
- add cleaning of records, or better archieving
- check wierd reporting of found new records for nepremicnine
- generalize both scrappers
- add filter changing (now it is fixed)
- add add to favorites and favorites filter
- add apartment size to the datamodel
- add enable and desable archieving
- add manual move to and from archive

IN PROGRESS
- Adding comment api

DONE
- deploy to some cloud infrastructire, preferablly AWS (gcp was chosen)
- Extract secrets and find a way to inject them
- Move to MySql
- extract parsers to separate files and module
- add docker builds only on selected tags (we are building only master branch instead)
- check wierd urls
- add commenting for choosen apartments

CANCELED
- Check how to add secrets to alembic
Docker commands:
```
sudo docker build -t wscr web_collector 
docker run -dit -p 5000:5000 wscr

sudo docker build -t wscr web_collector
docker run -dit --network wsc-network -p:5000:5000 --name wscr -v ~/software/python3/web_collector:/usr/code wscr 

gcloud app deploy
gcloud builds submit l5data/
gcloud app logs tail -s default
```
