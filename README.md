# Python Web Crawler

This web crawler attempts to crawl all the links from a website that share the same domain. The goal is to navigate to 
all the pages of a website and be able to only visit them once in a breadth first search manner.


## Set up enviroment

```bash
source venv/bin/activate && pip install -r requirements.txt
```

## Run crawler

Run the `src` package as a module and pass the url that you want to crawl as a first argument.

```bash
python -m src https://www.bbc.com/
```

## Run tests

```bash
pytest tests
```
