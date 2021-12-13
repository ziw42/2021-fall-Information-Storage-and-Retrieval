import requests

# reutrn {movie name: image url, movie url}
class CollaborationApi:
    def __init__(self, key):
        self.key = key
        self.base = "https://imdb8.p.rapidapi.com/"

    def do_retrieve(self, query, function):
        url = self.base + function
        querystring = query
        headers = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': self.key
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()

    def get_text(self, response, key):
        if key in response:
            return response[key]
        else:
            return None

    def get_id(self, name):
        query = {"q": name}
        response = self.do_retrieve(query, "auto-complete")
        if "d" in response:
            for t in response["d"]:
                return t["id"]
        else:
            return None

    def get_image_url(self, image):
        if image is not None:
            return image["url"]
        else:
            return None

    def get_movies_noname(self, ids):
        common_movies = {}
        if ids is not None:
            for i in range(len(ids)):
                if "nm" in ids[i]:
                    query = {"nconst": ids[i]}
                    response = self.do_retrieve(query, "actors/get-all-filmography")
                    movies = []
                    for work in self.get_text(response, "filmography"):
                        if work["titleType"] == 'movie':
                            if i == 0:
                                movies.append((work["title"], str(self.get_image_url(work.get("image")))+','+work["id"]))
                            else:
                                if work["title"] in common_movies.keys():
                                    movies.append((work["title"], str(self.get_image_url(work.get("image")))+','+work["id"]))
                    common_movies = dict(movies)
                    if not common_movies:
                        break

        return common_movies

    def get_collaboration(self, names):
        ids=[]
        for name in names.split(','):
            ids.append(self.get_id(name.strip()))
        return self.get_movies_noname(ids)
