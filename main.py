import webapp2, os, urllib2, urllib, json, jinja2, logging, api_key

omdb_api_key = api_key.omdb_api
movieDB_api_key = api_key.movieDB_api

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


# Handle any errors due to HTTP or connection related exceptions
def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        if hasattr(e, "code"):
            logging.error("The server couldn't fulfill the request.")
            logging.error("Error code: ", e.code)
        elif hasattr(e, 'reason'):
            logging.error("We failed to reach a server")
            logging.error("Reason: ", e.reason)
        return None


# Return a list of movie titles from the Movie Database API call
def getMovie(genre_id):
    baseurl = "http://api.themoviedb.org/3/discover/movie"
    param = {}
    param["api_key"] = movieDB_api_key
    param["sort_by"] = "popularity.desc"
    param["page"] = "1"
    param["with_genres"] = genre_id
    url = baseurl + "?" + urllib.urlencode(param)
    result = safeGet(url)
    if result is not None:
        movieData = json.load(result)
        sortedList = movieData["results"][0:5]
        # sortedList = sorted(movieData["results"], key=lambda x:x["vote_average"], reverse=True)[0:5]
        titleList = []
        for movie in sortedList:
            titleList.append(movie["title"])
        return titleList


# Return a dictionary with movie info data from the OMDb API call
def getMovieInfo(t="The Lion King"):
    base_url = 'http://www.omdbapi.com/'
    api_key = omdb_api_key
    api_key_str = '?apikey=' + api_key
    params = {}
    params['t'] = t  # movie title to search for
    paramstr = urllib.urlencode(params)
    omdbrequest = base_url + api_key_str + '&' + paramstr
    result = safeGet(omdbrequest)
    if result is not None:
        movieinfo_data = json.load(result)
        return movieinfo_data
    else:
        return "Sorry, couldn't retrieve the movie information."


# Define a movie class to get relevant, useful information about a movie
class Movie():
    def __init__(self, movie_dict):
        self.title = movie_dict['Title']
        self.rated = movie_dict['Rated']
        self.year = movie_dict['Year']
        self.runtime = movie_dict['Runtime']
        self.director = movie_dict['Director']
        self.actors = movie_dict['Actors']
        self.plot = movie_dict['Plot']
        self.poster = movie_dict['Poster']
        self.imdb_rating = movie_dict['imdbRating']
        self.imdb_votes = movie_dict['imdbVotes']
        self.imdb_id = movie_dict['imdbID']
        self.imdb_link = "https://www.imdb.com/title/" + self.imdb_id + "/"


# Define a class for the web application
class MainHandler(webapp2.RequestHandler):
    def get(self):
        vals = {}
        vals['page_title'] = "Moive Inspire Homepage"
        template = JINJA_ENVIRONMENT.get_template('landingpage.html')
        self.response.write(template.render(vals))

    def post(self):
        vals = {}
        vals['page_title'] = "Movie Inspire!"
        genre_id = self.request.get('genre')
        go = self.request.get("gobtn")
        logging.info(genre_id)
        logging.info(go)
        if genre_id:
            movieList = getMovie(genre_id=genre_id)
            movies = []
            for movie in movieList:
                if "Error" not in getMovieInfo(t=movie):
                    movies.append(Movie(getMovieInfo(t=movie)))
            # movies = [Movie(getMovieInfo(t=title)) for title in getMovie(genre_id=genre_id)]
            vals["movies"] = movies
            template = JINJA_ENVIRONMENT.get_template('outputpage.html')
            self.response.write(template.render(vals))
            logging.info('genre= ' + genre_id)


application = webapp2.WSGIApplication([('/', MainHandler), ('/results', MainHandler)], debug=True)
