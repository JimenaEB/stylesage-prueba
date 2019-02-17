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
    base_url = 'https://teatromadrid.com/p/cartelera-teatro-madrid/pagina/{page}'

    def start_requests(self):
        """Send petition to the first page that returns the play data"""
        yield scrapy.Request(url=self.base_url.format(page=1), callback=self.parse)

    def parse(self, response):
        """Extract info from the plays and call next page recursively"""
        box_info = response.selector.xpath('//*[@id="section-content"]/div/div[2]/a/@href').getall()
        if box_info:
            for box in box_info:
                yield scrapy.Request(url=box, callback=self.parse_detail)

            try:
                url_number = int(response.url.split('/')[-1]) + 1
            except:
                url_number = 2

            yield scrapy.Request(url=self.base_url.format(page=url_number), callback=self.parse)

    def parse_detail(self, response):
        """Extract the details of the plays based on if they are recomended"""
        if 'valoracion-palmas valoracioespectacle tooltip' in response.text:
            yield self.parse_recomended(response)
        else:
            yield self.parse_unrecomended(response)

    def parse_recomended(self, response):
        """Return recomended play data"""
        return {
            'play_name': response.selector.xpath('//*[@id="espetacle-header-compra"]/div/h1/text()').get(),
            'theatre': response.selector.xpath('//*[@id="main"]/article/div[1]/aside/div[1]/div[3]/p[2]/a/text()').get(),
            'genre': response.selector.css('#main > article > div.block > aside > div:nth-child(1) > div.dades > p.genere > span::text').get() or False,
            'dates': self.parse_dates(response.selector.xpath('//*[@id="main"]/article/div[1]/aside/div[1]/div[3]/p[1]/text()').get())
        }

    def parse_unrecomended(self, response):
        """Return unrecomended play data"""
        return {
            'play_name': response.selector.xpath('//*[@id="espetacle-header-compra"]/div/h1/text()').get(),
            'theatre': response.selector.xpath('//*[@id="main"]/article/div[1]/aside/div[1]/div[2]/p[2]/a/text()').get(),
            'genre': response.selector.css('#main > article > div.block > aside > div:nth-child(1) > div.dades > p.genere > span::text').get() or False,
            'dates': self.parse_dates(response.selector.xpath('//*[@id="main"]/article/div[1]/aside/div[1]/div[2]/p[1]/text()').get())
        }

    def parse_dates(self, dates):
        """Parse dates to page format to python date"""
        try:
            dates = dates.replace('\n', '').replace('Del ', '').replace('de ', '')
            date_start, date_end = dates.split(' al ')
            date_start = date_start.split(' ')
            date_end = date_end.split(' ')
            dates = {
                'start': date(day=int(date_start[0]), month=MONTH.get(date_start[1]), year=int(date_start[2])).strftime('%Y-%m-%d'),
                'end': date(day=int(date_end[0]), month=MONTH.get(date_end[1]), year=int(date_end[2])).strftime('%Y-%m-%d')
            }
        except:
            dates = 'Fecha desconocida'
        return dates
