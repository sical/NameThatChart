# NameThatChart

### website url : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/

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

### Quizz and task attribution

Once an user click on the start button from : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/ , he begins first, a small test to determine his knowledge.

This test, ask the user to complete few tasks. Each task answered right gives the user some points. those points allows us to estimate the user capacity and display adapted content.

To increase the accuracy of this process, the test use images ambiguous for common users like a "pareto chart" which can easily be mistaken for bar chart
or historical data visualization like Minard's map only known by experts.

This test class users into 3 categories :

- The "expert" this user can be trusted and might have more patience completing complexes tasks. In result, he will see more textual tasks and less swipes

-  The "average" this user will do a little of everything to keep him entertained, and still gives us valuable informations.

- The "basic" this will user might lack in domain knowledge to be dealing with complex graphs, however, he can still helps, he will more likely do swipes and selections.
