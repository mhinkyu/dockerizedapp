import gridfs
from urllib.request import urlopen
import pymongo


class Mongo:
    def __init__(self, ip, port, db_name, col_name):
        self.client = pymongo.MongoClient(ip, port)
        self.database = self.client[db_name]
        self.collection = self.database[col_name]
        self.gfs = gridfs.GridFS(self.database, collection=f'{col_name}')
    
    def insert_document(self,collection, document):
        use_collection = self.database[f'{collection}']
        insert_document = use_collection.insert_one(document)
        return insert_document.inserted_id
    
    def update_document(self, collection, field, query, new_values):
        use_collection = self.database[f'{collection}']
        myquery = {f'{field}': {'$regex' : f'{query}', '$options' :'i'}}
        newvalues = { "$set": new_values }
        use_collection.update_one(myquery, newvalues)
        output = {'Status': f'Successfully Updated {new_values}'}
        return output
    
    def delete_document(self, collection, field, query):
        use_collection = self.database[f'{collection}']
        use_collection.delete_one({f'{field}': {'$regex' : f'{query}', '$options' :'i'}})

    def save_url_images(self, images_dict):  
        movie_dict = {'name': f'{images_dict["name"]}', 'overview': f'{images_dict["overview"]}', 'rating': f'{images_dict["rating"]}', 'release': f'{images_dict["release_date"]}' }
        inserted_movie_id = self.insert_document('movies', movie_dict)
        for n, img_url in enumerate(images_dict['images'][:1]):
            img_file = urlopen(img_url)
            img_file_id = self.gfs.put(img_file)
            img_file_name = images_dict['name'] + str(n)
            print(f'{img_file_name} GOT SAVED IN THE DATABASE')
            self.database.imageMeta.insert_one({'moviename': images_dict['name'], 'filename': img_file_name, 'fileId': img_file_id, 'movie_Id': inserted_movie_id})
     


    def download_images(self, movie_name):
        doc = self.database.imageMeta.find_one({'moviename': {'$regex' : f'{movie_name}'}})
        print(doc)
        img = self.gfs.get(doc['fileId'])
        with open(f"{doc['filename']}.jpg", "wb+") as wf:
            wf.write(img.read())  

    def count_movies(self, movie_name):
        count = self.database.imageMeta.count_documents({'moviename': {'$regex' : f'{movie_name}', '$options' :'i'}})
        return count

    def get_image(self, movie_name):
        doc = self.database.imageMeta.find_one({'moviename': {'$regex' : f'{movie_name}', '$options' :'i'}})
        bin_img = self.gfs.get(doc['fileId'])
        bin_img_dict = {'moviename': f"{doc['moviename']}", 'bin_img': bin_img }
        movie_doc = self.database.movies.find_one({"name" : f"{doc['moviename']}"})
        bin_img_dict['rating'] = movie_doc['rating']
        bin_img_dict['overview'] = movie_doc['overview']
        bin_img_dict['release'] = movie_doc['release']
        return bin_img_dict
    
    def delete_image(self, collection, field, query):
        doc = self.database.imageMeta.find_one({f'{field}': {'$regex' : f'{query}'}})
        fileId = doc['fileId']
        self.delete_file(fileId, file_collection=collection)
        self.delete_document('imageMeta', 'moviename', query)
        output = {'Status': 'Successfully Deleted' if fileId  else "Nothing was Deleted."}
        return output

    def delete_file(self, fileId, file_collection=None ):
        self.gfs.delete(fileId)

if __name__ == "__main__":
    mongo = Mongo('localhost', 27017, 'movieland', 'movieposters')
