# Scraping Box Office Info with Scrapy
> Scraping the Box Office Mojo website with Scrapy

## The Goal of this Project
The goal of this project is to show the process of scraping web pages using Scrapy in Python. The web site scraped in this project is boxofficemojo.com. Especially, I check all the movies released in the US during certain periods of time and extract useful information about the individual movies. 

For each movie, the elements that I scrape here are ‘Domestic Revenues’, ‘Worldwide Revenues’, ‘Distributor’, ‘Opening’, ‘Budget’, ‘MPAA’, ‘Genres’, and ‘In Release’.

## How to Run this Project
- Install Python 3.
- Install the Python requirements with ```pip install -r requirements.txt```.
- Open a command line and go to the directory that you want to put your project into.
- Type this in the command line: ```C:\...> scrapy startproject boxofficeinfo```. A new folder named ```boxofficeinfo``` is automatically created.
- Using a text editor, open the file ```items.py```, ```pipelines.py```, and ```settings.py``` that were automatically created in the previous step. Replace the contents in those files for the contents in the files  ```items_contents.py```, ```pipelines_contents.py```, and ```settings_contents.py```, respectively.
- From the repository, download and save ```boxofficeinfo_spider.py``` into the ```spiders``` folder in the ```boxofficeinfo``` folder. 
- Navigate to ```boxofficeinfo``` directory in the command line.
```
boxofficeinfo>    scrapy.cfg
               boxofficeinfo>      _init_.py
                                    items.py
                              middlewares.py
                                pipelines.py
                                 settings.py
                                   _pycache_
                                     spiders> _init_.py
                                              _pycache_
```                                              
(As seen in the above, there are two ```boxofficeinfo``` directories. Navigate to the **upper** one between the two. ). 

- Then, type ```scrapy crawl Boxofficeinfo```.
- Check that ```boxoffice2017_2019.csv``` is created in the ```boxofficeinfo``` folder

(The whole process of writing codes for each file is explained in this link: https://medium.com/analytics-vidhya/scraping-box-office-info-with-scrapy-f23f1f2d684f)

## Result

![](https://github.com/yjeong5126/scraping_boxofficemojo/blob/master/images/7.PNG)
