import pip._vendor.requests as requests
import os
#from config import API_key as key
key = os.getenv('API_key')

class MOVIES:
    def __init__(self, movie_id = None, movie_name = None):
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.movie_rating = None
        self.overview = None
        self.release = None
        self.CONFIG_PATTERN = f'http://api.themoviedb.org/3/configuration?api_key={key}'
        self.get_movie_id()
        self.IMG_PATTERN = f'http://api.themoviedb.org/3/movie/{self.movie_id}/images?api_key={key}' 

    def get_json(self, url):
        r = requests.get(url)
        return r.json()

    def get_movie_id(self):
        if self.movie_id == None and self.movie_name != None:
            res = self.get_json(f'https://api.themoviedb.org/3/search/movie?api_key={key}&query={self.movie_name}')
            first_result = res['results']
            print('Response =>', first_result)
            self.movie_name = first_result[0]['original_title']
            self.movie_rating = first_result[0]['vote_average']
            self.overview = first_result[0]['overview']
            self.release = first_result[0]['release_date']
            self.movie_id = first_result[0]['id']

    # Depricated - for downloading to local machine, used for testing.
    def _download_images(self, urls, path='.'):
        for nr, url in enumerate(urls[0]):      # Using FOR - Later possibilty of downloading multiple images.
            r = requests.get(url)  
            filetype = r.headers['content-type'].split('/')[-1]
            filename = f'{self.movie_name}{nr+1}{filetype}'
            filepath = os.path.join(path, filename)
            with open(filepath,'wb') as w:
                w.write(r.content)

    def get_poster_urls(self):
        config_url = self.CONFIG_PATTERN
        config = self.get_json(config_url)
        base_url = config['images']['base_url']
        sizes = config['images']['poster_sizes']
        def size_str_to_int(x):
            return float("inf") if x == 'original' else int(x[1:])
        max_size = max(sizes, key=size_str_to_int)
        posters = self.get_json(self.IMG_PATTERN.format(movie_id=self.movie_id))["posters"]
        poster_urls = []
        for poster in posters:
            rel_path = poster['file_path']
            url = f'{base_url}{max_size}{rel_path}'
            poster_urls.append(url) 
        return poster_urls

    def get_images_dict (self):
        movie_images_urls = {
            'name': self.movie_name,
            'rating': self.movie_rating,
            'overview': self.overview,
            'release_date': self.release,
            'images': self.get_poster_urls()
        }
        return movie_images_urls

    # Depricated - for downloading to local machine, used for testing.
    def tmdb_posters(self, count=None, outpath='.'):    
        urls = self.get_poster_urls()
        if count is not None:
            urls = urls[:count]
        self._download_images(urls, outpath)

