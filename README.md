# NameThatChart

### website url : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/

## Using the dataset

If you want to download the data set we use, you can use our crawling tools located in the <a href="https://github.com/sical/NameThatChart/tree/master/datasetManager">datasetManager</a> directory.

This directory contains few tools :
    
    -   Crawling (crawl.py)
            This module allows an user to crawl google / wikipedia and bl.ock to get urls of the given names.
            
                args: {name: "--w", type: str, default: 'wikipedia', utility: select website to crawl from {'wikipedia','block','google'} }
                
                
    -   Crawling.d3js (d3jsdownload.py)
            This file can download all thumbnails / html files with meta data (name authors etc ..) from json files.
     
    -   Dataset
        -   Acutaldata contains the results of crawl.merge() consider this like final data.
        -   jsonCrawl contains result of one crawling session this is partial information.
        -   visCat contains the viscat datasets and we provide a tool to download them(vis10catDl.py slower than multidownload but easier to use). 
    
    
    -   Multidownload (ReaderDL.py)
        This module can read urls from a text file split this list to threads and download them.
        
          args: [ {name: "--input_file", type: str, default: 'vis10cat.txt', utility: select file where url are stored },
                  {name: "--output_dir", type: str, default: 'curent dir', utility: select directory to store ouput images},
                  {name: "--type", type: str, default: 'txt', utility: select type of given input file from : {"txt","json"}} ]
    
    - Azure    
        This script can be used to ask the azure congnitive search api to get url of images from a json file.
          args: [ {name: "--input_file", type: str, default: 'names.json', utility: select file where names are stored },
                  {name: "--output_file", type: str, default: 'imagesFromNames.json', utility: select the output file name and location be carefull it overwrites } ]
    
        
    - Chart names
        This dir contains 2 json files with  data visualization names:
             -cart.json contains names of a cartesian product from common chart suffix / prefix.
             
             -names.json contains the names of specifics graphs.
   
        
    Once you have gathered all data you want, you can : take it and feed them to readerDL.py to download and name them.
   
        
## Install and use Chrome app

In extension, this website have a chrome app extension which allow an user to capture a screen area and instantly upload it to our database in oder to discover how other users would have name this chart.

To install it, just drag and drop the app (NameThatChart-capture.crx located in the "Chrome app" folder) into chrome://extensions/ . 

## Understand web app structure

### Quizz and task attribution

Once an user click on the start button from : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/ , he begins a small test to determine his knowledge.

This test, ask the user to complete few tasks. Each task answered right gives the user some points. those points allows us to estimate the user capacity and display adapted content.

To increase the accuracy of this process, the test use images ambiguous for common users like a "pareto chart" which can easily be mistaken for bar chart
or historical data visualization like Minard's map only known by experts.

This test class users into 3 categories :

- The "expert" this user can be trusted and might have more patience completing complexes tasks. In result, he will see more textual tasks and less swipes

-  The "average" this user will do a little of everything to keep him entertained, and still gives us valuable informations.

- The "basic" this will user might lack in domain knowledge to be dealing with complex graphs, however, he can still helps, he will more likely do swipes and selections.

You can see bellow the points distribution:



|  tasks | Selection | Multiple | Swipes         | Textual |
|--------|-----------|----------|----------------|---------|
| points | 4         | 5        | 2 (per Chart) | 4       |




For a total of 23 points an user is : 

- an "Expert" for a grade higher than 18

- an "Average" from 18 points to 8

- and "Basic" bellow 8 points.


### Adding a new task

To add a new task, you must, first of all include the said page using specific css specified in  html style tag (increase perfs)

the said page must contain some of the elements down bellow :

- Grid blocks (classes "wrapper","main-nav","main-head","content","main-footer") 

- The main-nav must be filled with :

``` django
        {% if session.show %}
            {% include 'navbar.html' %}
        {% else %}
            {% include 'analytics.html' %}
        {% endif %}
```

- The tittle should have id="title"


- the footer must be filled with 

``` django
    {% include 'footer.html' %}
```

- This page should be in the nav bars ( links down bellow)

- This page must be map inside namethatchart.py
``` python

@application.route('/YourPage')

```

- any image of chart (``` <img> ```must have the attribute value = imageid) in order to have report working
 
- the Js loading this page must have a gethash, gen, skip, save function

- The main redirect should be handled ( look at other pages (js) )
 
- add this page to /main algorithm.



 > nav bars : https://github.com/sical/NameThatChart/blob/master/templates/navbar.html and https://github.com/sical/NameThatChart/blob/master/templates/nav.html


### Usefull links 


- To get all images class and their score : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/result

- to get raw images and where did we acquire them : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/image2json

- to get tasks logs in csv : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/datcsv.csv

- to get all reports in JSON : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/getreports

- to get global stats in JSON : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/getbasicstats

- to get tasks stats in JSON : http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/adminstats


