import scrapy

from datetime import date

MONTH = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}

class TheatreSpider(scrapy.Spider):
    name = "theatre"

    def start_requests(self):
        url = 'https://teatromadrid.com/p/cartelera-teatro-madrid/pagina/{page}'
        for page in range(1, 40):
            yield scrapy.Request(url=url.format(page=page), callback=self.parse)
            break

    def parse(self, response):
        box_info = response.selector.xpath('//*[@id="section-content"]/div/div[2]/a/@href').getall()
        for box in box_info:
            yield scrapy.Request(url=box, callback=self.parse_detail)

    def parse_detail(self, response):
        if 'valoracion-palmas valoracioespectacle tooltip' in response.text:
            play = self.parse_recomended(response)
        else:
            play = self.parse_unrecomended(response)


    def parse_recomended(self, response):
        play = {
            'name_play': response.selector.xpath('//*[@id="espetacle-header-compra"]/div/h1/text()').get(),
            'theatre': response.selector.xpath('//*[@id="main"]/article/div[1]/aside/div[1]/div[3]/p[2]/a/text()').get(),
            'genre': response.selector.css('#main > article > div.block > aside > div:nth-child(1) > div.dades > p.genere > span::text').get(),
            'dates': self.parse_dates(response.selector.xpath('//*[@id="main"]/article/div[1]/aside/div[1]/div[3]/p[1]/text()').get())
        }

    def parse_unrecomended(self, response):
        play = {
            'name_play': response.selector.xpath('//*[@id="espetacle-header-compra"]/div/h1/text()').get(),
            'theatre': response.selector.xpath('//*[@id="main"]/article/div[1]/aside/div[1]/div[2]/p[2]/a/text()').get(),
            'genre': response.selector.css('#main > article > div.block > aside > div:nth-child(1) > div.dades > p.genere > span::text').get(),
            'dates': self.parse_dates(response.selector.xpath('//*[@id="main"]/article/div[1]/aside/div[1]/div[2]/p[1]/text()').get())
        }

    def parse_dates(self, dates):
        dates = dates.replace('\n', '').replace('Del ', '').replace('de ', '')
        date_start, date_end = dates.split(' al ')
        date_start = date_start.split(' ')
        date_end = date_end.split(' ')
        dates = {
            'start': date(day=int(date_start[0]), month=MONTH.get(date_start[1]), year=int(date_start[2])),
            'end': date(day=int(date_end[0]), month=MONTH.get(date_end[1]), year=int(date_end[2]))
        }

        return dates
