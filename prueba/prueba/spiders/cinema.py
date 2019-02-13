import scrapy
import json

class CinemaSpider(scrapy.Spider):
    name = "cinema"

    def start_requests(self):
        url = 'http://www.yelmocines.es/now-playing.aspx/GetNowPlaying'
        yield scrapy.Request(
            url=url, callback=self.parse, method='POST',
            headers={'Content-Type': "application/json; charset=UTF-8"},
            body=json.dumps({'cityKey': 'madrid'})
        )

    def parse(self, response):
        info = json.loads(response.text)
        cinemas = info.get('d').get('Cinemas')
        parsed_cinemas = []

        for cinema in cinemas:
            parsed_cinemas.append(self.parse_cinemas(cinema))

    def parse_cinemas(self, cinema):
        cine = {
            'cinema_name' : cinema.get('Name'),
            'movies' : self.get_movies(cinema.get('Dates'))
        }
        print(json.dumps(cine))
        return cine

    def get_movies(self, dates):
        parsed_movies = {}

        for date in dates:
            show_date = date.get('ShowtimeDate')
            
            for movie in date.get('Movies'):
                if movie.get('Title') in parsed_movies:
                    parsed_movies[movie.get('Title')]['show_date'].append(show_date)
                else:
                    parsed_movies[movie.get('Title')] = {
                        'rating': movie.get('RatingDescription'),
                        'gender': movie.get('Gender'),
                        'sypnosis': movie.get('Synopsis'),
                        'show_date': [show_date]
                    }

        return parsed_movies
