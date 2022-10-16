import codecs
from flask import Flask, jsonify, redirect, render_template, request, url_for
from bs4 import BeautifulSoup as BSHTML
import IMDBapp
import Mongoapp


app = Flask(__name__)

# my_mongo = Mongoapp.Mongo('172.24.2.2', 27017, 'movieland', 'movieposters')
my_mongo = Mongoapp.Mongo('localhost', 27017, 'movieland', 'movieposters')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/qposter', methods = ['POST', 'GET'])
def get_poster_req():
    if request.method == 'POST':
      query_movie = request.form['query_movie']
      return redirect(url_for('get_poster',movie_name = query_movie))
    else:
      query_movie = request.args.get('query_movie')
      return redirect(url_for('get_poster',movie_name = query_movie))

@app.route('/updatemovie', methods = ['POST'])
def update():
    edited_title = request.form['editTitle']
    edited_overview = request.form['editOverview']
    current_name = request.form['currentName']
    edit_dict = {
        'name': edited_title,
        'overview': edited_overview
    }
    edit_meta_dict = {
        'moviename': edited_title,
        'filename': f'{edited_title}0'
    }
    my_mongo.update_document('movies', 'name', current_name, edit_dict )
    my_mongo.update_document('imageMeta', 'moviename', current_name, edit_meta_dict )
    return redirect(url_for('index'))

@app.route('/deletemovie', methods = ['POST'])
def delete():
    req_data = request.json
    title = req_data['name']
    status = my_mongo.delete_image('movieposters.files', 'moviename', title)
    my_mongo.delete_document('movies', 'name', title)
    return status


@app.route('/poster/<movie_name>', methods = ['GET'])
def get_poster(movie_name):
    movie_count = my_mongo.count_movies(movie_name)
    print('Amount of posters in database : ', movie_count)
    if movie_count != 0:
        db_img_meta = my_mongo.get_image(f'{movie_name}')
        bin_img = db_img_meta['bin_img']
        base64_data = codecs.encode(bin_img.read(), 'base64') 
        image = base64_data.decode('utf-8')
        res_dict = {
            'image': image,
            'name': db_img_meta['moviename'],
            'rating': db_img_meta['rating'],
            'overview': db_img_meta['overview'],
            'release': db_img_meta['release']
        }
    else:
        search_movie = IMDBapp.MOVIES(movie_name=f'{movie_name}')
        movie_posters = search_movie.get_images_dict()
        my_mongo.save_url_images(movie_posters)
        return get_poster(movie_posters['name'])
    return jsonify(res_dict)

@app.route('/posters/<movie_name>', methods = ['GET'])
def get_posters(movie_name):
    movie_count = my_mongo.count_movies(movie_name)
    print('Amount of posters in database : ', movie_count)
    if movie_count != 0:
        db_img_meta = my_mongo.get_image(f'{movie_name}')
        bin_img = db_img_meta['bin_img']
        base64_data = codecs.encode(bin_img.read(), 'base64') 
        image = base64_data.decode('utf-8')
    else:
        search_movie = IMDBapp.MOVIES(movie_name=f'{movie_name}')
        movie_posters = search_movie.get_images_dict()
        my_mongo.save_url_images(movie_posters)
        print(f'HERE I AM  $$$$$=> {movie_posters["name"]}')
        return get_poster(movie_posters['name'])
    return f'<h2>{db_img_meta["moviename"]}</h2><img src = "data:image/png;base64, {image}" style="display: block; margin-left: auto; margin-right: auto; width: 50%; " alt= "myImage" />'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug = True)
