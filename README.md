# NameThatChart

## Using the dataset

if you want to download the dataset we use you can use our crawling tools located in the datasetManager direcory.

This directory contains few tools :
    
    -   Crawling (crawl.py)
            This module allows an user to crawl google / wikipedia and bl.ock to get urls of the given names
        
    -   Crawling.d3js (d3jsdownload.py)
            This file can download all thumbnails / html files with meta data (name authors etc ..) from json files
     
    -   dataset
        -   Acutaldata contains the results of crawl.merge() consider this like final data
        -   jsonCrawl contains result of one crawling session this is partial information.
        -   visCat contains the viscat datasets and we provide a tool to download them(vis10catDl.py). 
    
    -   multidownload
        This module can read urls from a text file split this list to threads and download them.
   
        
##Install and use Chrome app


## Understand web app structure