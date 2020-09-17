# Scraping Box Office Info with Scrapy
> Scraping the Box Office Mojo website with Scrapy

## The Goal of this Project
The goal of this project is to show the process of scraping web pages using Scrapy in Python. The web site scraped in this project is boxofficemojo.com. Especially, I check all the movies released in the US during certain periods of time and extract useful information about the individual movies. 

For each movie, you will see the page as follows:

![](https://github.com/yjeong5126/scraping_boxofficemojo/blob/master/images/1.PNG)

The elements that I scrape here are ‘Domestic Revenues’, ‘Worldwide Revenues’, ‘Distributor’, ‘Opening’, ‘Budget’, ‘MPAA’, ‘Genres’, and ‘In Release’.

## Creating a New Project
Once you finished installing Scrapy on your python, let’s create a new project for scraping the web. Open a command line and go to the folder that you want to put your project into. Then, type this:
```
C:\...> scrapy startproject boxofficeinfo
```
```scrapy startproject``` is the command for creating and starting a new project. Replace ```boxofficeinfo``` with your own project name. Once you are successful for creating the project, you will see the following message saying that now you can start your first spider:
```
...
...\ ...\ boxofficeinfo
You can start your first spider with:
    cd boxofficeinfo
    scrapy genspider example example.com
```
At the same time, Scrapy creates a new folder containing several files and sub-folders necessary for the web scraping. Since I named my new project ‘boxofficeinfo’, the new folder created has the name, ‘boxofficeinfo’.
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
Now, we are ready to start scraping the web. The whole process for the web scraping via Scrapy involves the following steps:
- Writing on items.py
- Creating Spider(.py) and Identifying the Patterns of the Web
- Writing on pipelines.py
- Changing setting in Settings.py
- Running the Scrapy!

## items.py
Let’s start with working on ```items.py``` first. In ```items.py```, we will designate which information in the web will be extracted and stored. Among many information about the movies on this site, we will extract information about ‘Domestic Revenues’, ‘Worldwide Revenues’, ‘Distributor’, ‘Opening’, ‘Budget’, ‘MPAA’, ‘Genres’, and ‘In Release’ for individual movies. This is the contents my ```items.py``` has in the file:
```
import scrapy

class BoxofficeItem(scrapy.Item):
    title = scrapy.Field()
    domestic_revenue = scrapy.Field()
    world_revenue = scrapy.Field()
    distributor = scrapy.Field()
    opening_revenue = scrapy.Field()
    opening_theaters = scrapy.Field()
    budget = scrapy.Field()
    MPAA = scrapy.Field()
    genres = scrapy.Field()
    release_days = scrapy.Field.()
```
## Creating your Spider(.py) and Identifying the Pattern of the Web
The next thing we need to do is to create our spider. The file for the spider is not automatically created by Scrapy. Open a new file in your python text editor and save the file with your own name into ```spiders``` folder. For convenience’s sake, I named the file ```boxofficeinfo_spider.py.``` This is how I started with my spider:
```
import scrapy
from boxofficeinfo.items import BoxofficeItem

class BoxofficeSpider(scrapy.Spider):
    name = "Boxofficeinfo"
    allowed_domains = ["boxofficemojo.com"]
    start_urls = [
    "https://www.boxofficemojo.com/year/2017/"
    ]
```
First, I imported ```scrapy``` and ```BoxofficeItem``` that was created in the previous stage. The next thing we do here is to give our spider its ```name```, designate the ```allowed_domains```, and set the ```start_urls```. The URLs in the ```start_urls``` are supposed to be where your scraping starts.

![](https://github.com/yjeong5126/scraping_boxofficemojo/blob/master/images/2.PNG)

```start_urls``` can contain more than one URLs. What if we want to extract the same information for the movies in 2018 and 2019 as well? Then, simply add the URLs for those pages into ```start_urls```. In some cases, you can use the next or previous page button in order to move onto those pages. Here, we will use the URL directly. You can see that ```www.boxofficemojo.com/year/2017/``` contains ‘2017’, which means that we can move to the pages for other years by changing this number. Let’s add the URLs for year 2018 and 2019 in the following way:
```
start_urls = [
    "https://www.boxofficemojo.com/year/2017/"
    ]
    
for year in [2018, 2019]:
    start_urls.append("https://
                       www.boxofficemojo.com/year/"+str(year)+"/")
```
The next thing to do in creating our spider is to define ```parse``` function which directs our spider on how to scrape the web. Before setting how to parse the web, it’s necessary for us to identify the pattern of the web in advance.

The movie information that we want to extract is not shown directly on the main page. (From now on, I will call the pages in the ```start_urls``` the ‘main page(s)’.) Basically, we can get to the pages for the individual movies via using their URLs. For example, the URL for the first movie on the list, ‘Star Wars: Episode VIII — The Last Jedi’ , is ```https://www.boxofficemojo.com/release/rl2708702721/?ref_=bo_yld_table_1```. Then, how can we get this URL for all the movies? The main page has all the links to the individual movies, which means that the main page contains all the URLs for the movies. Therefore, we can get those URLs through inspecting the HTML of the main page.

The best way to find out the URLs in the HTML is to use Scrapy Shell. In the command line, type this:
```
> scrapy shell "https://www.boxofficemojo.com/year/2017/"
....<scraped contents>...
......
In [1]:_
```
The Scrapy scraped the whole page of the URL we entered. The next thing to do is to find the xpath to the link to the individual movies. The xpath can be found by using Inspect on Chrome.

![](https://github.com/yjeong5126/scraping_boxofficemojo/blob/master/images/3.png)

The xpath that was copied above is ```‘//[@id=”table”]/div/table[2]/tbody/tr[2]/td[2]/a’```. Now, type this to see if this xpath gives what we want:
```
> scrapy shell "https://www.boxofficemojo.com/year/2017/"
....<scrapped contents>...
......
In [1]: response.xpath('//[@id=”table”]/
                                   div/table[2]/tbody/tr[2]/td[2]/')
Out [1]: []
```
It gives nothing! Keep in mind that in many cases the xpath we find through the method we did previously is not always correct. We need to find the correct one manually based on the copied xpath in the previous stage.

I found the correct xpath after several trials.
```
> scrapy shell "https://www.boxofficemojo.com/year/2017/"
.....
.....
In [4]: response.xpath('//*[@id="table"]/div/table/tr[2]/td[2]/a/@href')[0].extract()
Out[4]: '/release/rl2708702721/?ref_=bo_yld_table_1' 
```
In ```out[4]```, I was successful in extracting the relative URL for the ‘Star Wars: Episode VIII’. Using ```urljoin```, we can combine our relative URL we found here with the base URL.
```
In [5]: response.urljoin('/release/rl2708702721/?ref_=bo_yld_table_1')
Out [5]:'https://www.boxofficemojo.com/release/rl2708702721/? ref_=bo_yld_table_1'
```
Now, we are able to obtain the URL for one individual movie we chose. Then, how can we obtain the URLs for the whole movies in the list? For this, let’s check the HTML of the main page again in order to see some pattern of the page.

![](https://github.com/yjeong5126/scraping_boxofficemojo/blob/master/images/4.png)

The information for each movie is contained in the ```<tr>…</tr>``` tag, and each ```<tr>…</tr>``` tag has the same format. Therefore, to find out all the links for the individual movie, type the following code:
```
def parse(self, response):
    for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:]:
        href = tr.xpath('./td[2]/a/@href')
        url = response.urljoin(href[0].extract())
        yield scrapy.Request(url, callback=self.parse_page_contents)
```
Now, we figured out how to get to the page for each movie in the list. ```scrapy.Request``` that we typed above will parse each ```url``` following ```parse_page_contents``` function we define in the next step.

The ```parse_page_contents``` function has the format like the following:
```
def parse(self, response):
    for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:]:
        href = tr.xpath('./td[2]/a/@href')
        url = response.urljoin(href[0].extract())
        yield scrapy.Request(url, callback=self.parse_page_contents)
def parse_page_contents(self, response):
    item = BoxofficeItem()
    item["title"] =
    item["domestic_revenue"] = 
     ...
    item["release_days"] = 
    yield item
```
In the ```parse_page_contents```, we determine what information will be put in each element in the items. In our case, what we want to put in ```item[“domestic_revenue”]``` should be the domestic revenue for each movie. Since the format and pattern of the pages for individual movies are very similar, once we figure out the location where the information for the domestic revenue is stored for one movie, we will be able to apply this location to the other movies.

![](https://github.com/yjeong5126/scraping_boxofficemojo/blob/master/images/5.PNG)

The domestic revenue for ‘Star Wars: Episode VIII’, is ‘$620,181,382. The xpath for this information is ```'//*[@id=”a-page”]/main/div/div[3]/div[1]/div/div[1]/span[2]/span’```. Using scrapy shell for the page above, we can see the following command is corresponding to the number for the domestic revenue:
```
In [2]: response.xpath('//*[@id=”a-page”]/main/div/div[3]/div[1]/div/div[1]/span[2]/span/text()')[0].extract()
Out [2]: '$620,181,382'
```
Basically, this command can be applied to the other movies as well because this information will be located in the same place for any other movies. Therefore, we can use this command for ```item[“domestic_revenue”]```.
```
def parse_page_contents(self, response):
    item = BoxofficeItem()
    item["title"] = 
    item["domestic_revenue"] = response.xpath('//*[@id=”a-page”]/main/div/div[3]/div[1]/div/div[1]/span[2]/span/text()')[0].extract()
     ...
    item["release_days"] = 
    yield item
```
What about “Genres”? In the case for ‘Star Wars: Episode VIII’, the information about “Genres” is located at this xpath: ```‘//*[@id=”a- page”]/main/div/div[3]/div[4]/div[7]/span[2]’```. Let’s use this xpath for “Genres”.
```
In [3]: response.xpath('//*[@id="a-     page"]/main/div/div[3]/div[4]/div[7]/span[2]/text()')[0].extract()
Out [3]: 'Action\n    \n        Adventure\n    \n        Fantasy\n    \n        Sci-Fi' 
```
The visual we want for this information is ```‘Action,Adventure,Fantasy,Sci-Fi’``` without the extra spacing. Therefore, we can change the command like the following:
```
In [4]: ",".join(response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div[7]/span[2]/text()')[0].extract().split())
Out [4]: 'Action,Adventure,Fantasy,Sci-Fi'
```
Therefore, we can type ```item[“genres”]= “,”.join(response.xpath(‘//*[@id=”a-page”]/main/div/div[3]/div[4]/div[7]/span[2]/text()’)[0].extract().split())``` for “Genres”. We can do the similar things for the rest of the information to complete the ```parse_page_contents``` function.

## Challenge for Scraping Box Office Mojo
The completed format of our spider will be like the following format:
```
import scrapy 
from Boxoffice.items import BoxofficeItem
class BoxofficeSpider(self, response):
    name = "..."
    allowed_domains = ["..."]
    start_urls = ["..."]
    def parse(self,response):
        ...
        yield scrapy.Request(url, callback=self.parse_page_contents)
    def parse_page_contents(self, response):
        item = BoxofficeItem()
        item["title"] = ...
        ...
        item["release_days"] = ...
        yield item
```
However, this code only works when the information for all individual movies is located in the same place on each page. For example, the page for ‘Naples ’44' is like the following:

![](https://github.com/yjeong5126/scraping_boxofficemojo/blob/master/images/6.PNG)

It does not contain the information about ‘Budget’ and ‘MPAA’. If we run the code that we made earlier, it will create wrong information or make errors. For example, this page does not provide any information about ‘MPAA’. The ```item[‘MPAA’]``` for this movie should be ```‘N/A’```. However, if we type
```
item["MPAA"] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div[5]/span[2]/text()')[0].extract()
```
following the information from ‘Star Wars: Episode VIII’, in which ‘MPAA’ is in the fifth row, ‘Documentary War’ will be entered into ‘MPAA’ like this: ```item[“MPAA”]=‘Documentary War’```. Therefore, when we extract the information we need, we should consider whether all the elements are included or not in each movies.

My strategy to solve this problem is to type this:
```
elements = []
for div in response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div')[0:]:
        elements.append(' '.join(div.xpath('./span[1]/text()')[0].extract().split()))
```
Let’s run this code after running scrapy shell for the movie, ‘Naples ’44'.
```
> scrapy shell "https://www.boxofficemojo.com/release/rl1812104705/weekend/"
....
In [1]: elements = []
In [2]: for div in response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div')[0:]: elements.append(' '.join(div.xpath('./span[1]/text()')[0].extract().split()))
In [3]: elements
Out [3]: ['Distributor','Opening','Release Date','Running Time','Genres','In Release','Widest Release','IMDbPro']
```
The output gives us the information about which elements are included in this movie and in what order each element is. So, type the following for ```item[“MPAA”]```:
```
if 'MPAA' in elements:
    m = elements.index('MPAA') + 1
    loc_MPAA = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(m)
    item["MPAA"] = response.xpath(loc_MPAA)[0].extract()
else:
    item["MPAA"] = "N/A"
```
If the page for a movie includes ‘MPAA’, it will give the correct information about ‘MPAA’. Otherwise, ```‘N/A’``` will be entered.

## pipelines.py and settings.py
Once we finished writing the code for ```items.py``` and ```spider.py```, we are ready to scrape the web and extract the data we want. However, using ```pipelines.py```, we can determine the setting in the csv file. This is the csv file setting that we use for this project. Opening ```pipelines.py``` which was automatically created by Scrapy, write down the code as follows:
```
import csv
class YourPipelineName(object):
    def __init__(self):
        self.csvwriter = csv.writer(open("boxoffice2017_2019.csv", "w", newline=''))
        self.csvwriter.writerow(["title", "domestic_revenue", "world_revenue", "distributor", "opening_revenue", "opening_theaters", "budget", "MPAA", "genres", "release_days"])
    def process_item(self, item, spider):
        row = []
        row.append(item["title"])
        row.append(item["domestic_revenue"])
        row.append(item["world_revenue"])
        row.append(item["distributor"])
        row.append(item["opening_revenue"])
        row.append(item["opening_theaters"])
        row.append(item["budget"])
        row.append(item["MPAA"])
        row.append(item["genres"])
        row.append(item["release_days"])
        self.csvwriter.writerow(row)
        return item
```
To apply the setting we created above, we have one thing to change in ```settings.py```. In the middle of the ```settings.py```, we need to activate ```ITEM_PIPELINES = {….}```.
```
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Boxoffice2019.pipelines.YourPipelineName': 300,
}
```
Make sure that you need to replace ```YourPipelineName``` with the name you made for the pipelines.

## Run the Spider!!
Now it’s time to run the code we created to extract all the information for the movies. We need to navigate to ```boxofficeinfo``` folder. Then, type the following:
```
..\Boxofficeinfo> scrapy crawl Boxofficeinfo
```
```Boxofficeinfo``` we typed after ```scrapy crawl``` is the spider name we made in our ```Spider.py```. Then, the ```boxoffice2017_2019.csv``` is created in the ```Boxofficeinfo``` folder.

![](https://github.com/yjeong5126/scraping_boxofficemojo/blob/master/images/7.PNG)
























    





























