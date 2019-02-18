# stylesage-prueba
Proyecto hecho como prueba técnica para la empresa Stylesage.

Consiste en dos spiders que recogen datos de webs de ocio de Madrid, uno de Teatros Madrid y otro de Yelmo cines Madrid. 
Esta información se vuelca en Dynamodb y se accede a ella mediante lambdas conectadas a una API Gateway.

## Scraper
El scraper se apoya en Scrapy y está formado por dos spiders:

### Cinema
Hace una petición a http://www.yelmocines.es/now-playing.aspx/GetNowPlaying y descarga un JSON 
del que va extrayendo la información de las películas que se proyectan en cada cine.

### Theatre
Recorre la web https://teatromadrid.com/p/cartelera-teatro-madrid navegando por la paginación dinámica y
entrando en cada URL de una obra para extraer la información de las obras.

## Dynamodb
Se ha elegido Dynamodb como base de datos porque es serverless y escala igual que las lambdas, así se evitan 
cuellos de botella

## Lambdas
Se han creado cuatro lambdas alojadas en AWS para acceder a la información de Dynamodb:

### get_theatres
Realiza una petición GET a https://dhqcbeuzy9.execute-api.eu-west-3.amazonaws.com/test/theatres
para obtener una lista con todos los teatros de Madrid.
Devuelve un diccionario con una lista de teatros y el número total de teatros.

### get_plays
Realiza una petición GET a https://dhqcbeuzy9.execute-api.eu-west-3.amazonaws.com/test/plays
para obtener todas las obras de teatro, y su información, que hay en Madrid.
Devuelve un diccionario con un diccionario con toda la información de las obras y el número total de obras.

### get_cinemas
Realiza una petición GET a https://dhqcbeuzy9.execute-api.eu-west-3.amazonaws.com/test/cinemas
para obtener una lista con todos los cines de Madrid.
Devuelve un diccionario con una lista de cines y el número total de cines.

### get_movies_by_cinema
Realiza una petición POST a https://dhqcbeuzy9.execute-api.eu-west-3.amazonaws.com/test/cinemas/movies pasándole un
diccionario con el nombre del cine cómo parámetro.
Devuelve un diccionario con un diccionario que contiene toda la información de las películas y el total de películas disponibles en ese cine.


## Api Gateway
Expone las lambdas mediante una URL para poder acceder a ellas. Sus métodos son:
- /cinemas
- /cinemas/movies
- /plays
- /theatres
