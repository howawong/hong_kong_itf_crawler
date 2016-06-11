# hong_kong_itf_crawler
Web Crawler of http://www.itf.gov.hk/l-tc/Prj_Search.asp?code=108

## Run
```bash
python scraper.py  #crawl data from the internet and projects_uncleansed.json is produced.
python cleanser.py #cleanse projects_uncleansed.json and projects.json is produced.
```

##Dependency
json lxml requests
