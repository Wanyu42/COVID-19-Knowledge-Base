# COVID-19-Knowledge-Base

2020-2021 FYP Code: SYQ4

## Project Description

This project builds a domain-specific search engine for COVID-19 academic papers. The data used consists of over 80,000 paper information and over 180,000 chemicals and diseases.
The project consists of four major components: Paper Crawler, Database Management, Learning to Rank, and Front-end.

### Paper Crawler
The papers were crawled in PubMed website. The seed papers pmid are from UIUC dataset. 
To speed up the networking, we used asynchronous request to crawl the pages. The crawled infomation was stored in sqlite database. Details are in WebCrawlerSQL.py.

### Database Management
We used Neo4j NoSQL database to store the graph relations between different chemicals and diseases. The dataset are from UIUC. The construction of the database is shown in CSVReader.py.
The query of the database is implemented in GraphQueryClass.py. Neo4j is based on the community version 4.x. To launch the database, run the following in Windows:

>neo4j console

### Learning to Rank
To rank the retrieved result, we used natural language processing to represent the documents as vector based on their titles and abstracts. 
The learning part is stored in "learning" folder. In essense, we used quickthought model to get the document vector. 

### Front-end
The website is built based on Flask framework. The web service is launched through app.py. The following code is run in Windows:


  >set FLASK_APP=app.py\n
  
  >flask run
