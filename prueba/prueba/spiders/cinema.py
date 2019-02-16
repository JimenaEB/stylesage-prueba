import scrapy
import json

class CinemaSpider(scrapy.Spider):
    name = "cinema"

    def start_requests(self):
        """Send the petition to the endpoint that returns the cinema data"""
        url = 'http://www.yelmocines.es/now-playing.aspx/GetNowPlaying'
        yield scrapy.Request(
            url=url, callback=self.parse, method='POST',
            headers={'Content-Type': "application/json; charset=UTF-8"},
            body=json.dumps({'cityKey': 'madrid'})
        )

    def parse(self, response):
        """Extract the data from response"""
        info = json.loads(response.text)
        cinemas = info.get('d').get('Cinemas')

        for cinema in cinemas:
            yield self.parse_cinemas(cinema)

    def parse_cinemas(self, cinema):
        """Extract the data from a single cinema"""
        cine = {
            'cinema' : cinema.get('Name'),
            'movies' : self.get_movies(cinema.get('Dates'))
        }
        print(json.dumps(cine))
        return cine

    def get_movies(self, dates):
        """Extract all the data from the movies at a single cinema"""
        parsed_movies = {}

        for date in dates:
            show_date = date.get('ShowtimeDate')

            for movie in date.get('Movies'):
                if movie.get('Title') in parsed_movies:
                    parsed_movies[movie.get('Title')]['show_date'].append(show_date)
                else:
                    parsed_movies[movie.get('Title')] = {
                        'rating': movie.get('RatingDescription') or None,
                        'gender': movie.get('Gender') or None,
                        'sypnosis': movie.get('Synopsis') or None,
                        'show_date': [show_date]
                    }

        return parsed_movies
