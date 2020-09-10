import scrapy

from boxofficeinfo.items import BoxofficeItem

class BoxofficeSpider(scrapy.Spider):
    name = "Boxofficeinfo"
    allowed_domains = ["boxofficemojo.com"]
    start_urls = [
    "https://www.boxofficemojo.com/year/2017/"
    ]

    for year in [2018, 2019]:
        start_urls.append("https://www.boxofficemojo.com/year/"+str(year)+"/")

    def parse(self, response):
        for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:]:
            href = tr.xpath('./td[2]/a/@href')
            url = response.urljoin(href[0].extract())
            yield scrapy.Request(url, callback=self.parse_page_contents)

    def parse_page_contents(self, response):
        item = BoxofficeItem()
        item["title"] = response.xpath('//*[@id="a-page"]/main/div/div[1]/div[1]/div/div/div[2]/h1/text()')[0].extract()
        item["domestic_revenue"] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[1]/div/div[1]/span[2]/span/text()')[0].extract()
        item["world_revenue"] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[1]/div/div[3]/span[2]/a/span/text()')[0].extract()

        elements = []
        for div in response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div')[0:]:
            elements.append(' '.join(div.xpath('./span[1]/text()')[0].extract().split()))

        #Distributor
        if 'Distributor' in elements:
            d = elements.index('Distributor') + 1
            loc_dist = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(d)
            item["distributor"] = response.xpath(loc_dist)[0].extract()
        else:
            item["distributor"] = "N/A"

        # Opening Revenue
        if 'Opening' in elements:
           o = elements.index('Opening') + 1
           loc_open_rev = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/span/text()'.format(o)
           try:
               item["opening_revenue"] = response.xpath(loc_open_rev)[0].extract()
           except:
               item["opening_revenue"] = "N/A"
        else:
            item["opening_revenue"] = "N/A"

        # Opening Theaters
        if 'Opening' in elements:
           o = elements.index('Opening') + 1
           loc_open_theater = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(o)
           try:
               item["opening_theaters"] = response.xpath(loc_open_theater)[0].extract().split()[0]
           except:
               item["opening_theaters"] = "N/A"
        else:
            item["opening_theaters"] = "N/A"

        # Budget
        if 'Budget' in elements:
            b = elements.index('Budget') + 1
            loc_budget = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/span/text()'.format(b)
            item["budget"] = response.xpath(loc_budget)[0].extract()
        else:
            item["budget"] = "N/A"

        # MPAA
        if 'MPAA' in elements:
            m = elements.index('MPAA') + 1
            loc_MPAA = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(m)
            item["MPAA"] = response.xpath(loc_MPAA)[0].extract()
        else:
            item["MPAA"] = "N/A"

        # Genres
        if 'Genres' in elements:
            g = elements.index('Genres') + 1
            loc_genres = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(g)
            item["genres"] = ",".join(response.xpath(loc_genres)[0].extract().split())
        else:
            item["genres"] = "N/A"

        # In Release
        if 'In Release' in elements:
            r = elements.index('In Release') + 1
            loc_release = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(r)
            item["release_days"] = response.xpath(loc_release)[0].extract().split()[0]
        else:
            item["release_days"] = "N/A"
        yield item
