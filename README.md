# NameThatChart

### website url : https://namethatchart.herokuapp.com

## Using the dataset

if you want to download the data set we use you can use our crawling tools located in the datasetManager directory.

This directory contains few tools :
    
    -   Crawling (crawl.py)
            This module allows an user to crawl google / wikipedia and bl.ock to get urls of the given names
        
    -   Crawling.d3js (d3jsdownload.py)
            This file can download all thumbnails / html files with meta data (name authors etc ..) from json files
     
    -   dataset
        -   Acutaldata contains the results of crawl.merge() consider this like final data
        -   jsonCrawl contains result of one crawling session this is partial information.
        -   visCat contains the viscat datasets and we provide a tool to download them(vis10catDl.py slower than multidownload but easier to use). 
    
    
    -   multidownload
        This module can read urls from a text file split this list to threads and download them.
   
        
## Install and use Chrome app

In extention, this website have a chrome app extention which allow an user to capture a screen area and instantly upload it to our databse in oder to discover what others would name this chart.

To install it, just drag and drop the app (NameThatChart-capture.crx located in the "Chrome app" folder) into chrome://extensions/. 

## Understand web app structure

