import requests
from ActorApi import ActorApi

class FilmApi:
    def __init__(self, key):
        self.key = key
        self.base = "https://imdb8.p.rapidapi.com/"

    def do_retrieve(self, query, function):
        url = self.base + function
        headers = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': self.key
        }
        response = requests.request("GET", url, headers=headers, params=query)
        return response.json()

    def get_id(self, name):
        query = {"q":name}
        response = self.do_retrieve(query, "auto-complete")
        if "d" in response:
            ids = []
            for t in response["d"]:
                ids.append(t["id"])
            return ids
        else:
            return None

    def get_image_url(self, image):
        if image is not None:
            return image["url"]
        else:
            return None

    def get_text(self, response, key):
        if key in response:
            return response[key]
        else:
            return None

    def get_intruduction(selfself, plotSummary):
        if plotSummary is not None:
            return plotSummary["text"]
        else:
            return None

    def get_intro(self, name):
        intro = []
        query = {"q":name}
        response = self.do_retrieve(query, "title/find")
        actorApi = ActorApi("db57077c0emsh6e14bcb6ea8184ep1f3388jsn8093fce376d1")
        if "results" in response:
            for t in response["results"]:
                if "tt" in t["id"]:
                    query_2 = {"tconst":t["id"].replace("/", "").replace("title",""),"currentCountry":"US"}
                    response_2 = self.do_retrieve(query_2, "title/get-overview-details")
                    rating = self.get_rating(t["id"])
                    temp = {"title": self.get_text(t, "title"), "type": self.get_text(t, "titleType"),
                            "year": self.get_text(t, "year"), "principals": self.get_text(t, "principals"),
                            "image": self.get_image_url(self.get_text(t, "image")),
                            "rating": rating, "introduction": self.get_intruduction(self.get_text(response_2, "plotSummary")),
                            "id": t["id"]}
                    intro.append(temp)
        intro = sorted(intro, key = lambda i: i["year"], reverse = True)
        return intro

    def get_rating_value(self, rating):
        if rating == None:
            return 0
        else:
            return rating

    def get_intro_limited(self, name, num):
        n = 0
        intro = []
        query = {"q": name}
        response = self.do_retrieve(query, "title/find")
        actorApi = ActorApi("db57077c0emsh6e14bcb6ea8184ep1f3388jsn8093fce376d1")
        if "results" in response:
            for t in response["results"]:
                if n < num:
                    if "tt" in t["id"]:
                        query_2 = {"tconst": t["id"].replace("/", "").replace("title", ""), "currentCountry": "US"}
                        response_2 = self.do_retrieve(query_2, "title/get-overview-details")
                        rating = self.get_rating(t["id"])
                        temp = {"title": self.get_text(t, "title"), "type": self.get_text(t, "titleType"),
                                "year": self.get_text(t, "year"), "principals": self.get_text(t, "principals"),
                                "image": self.get_image_url(self.get_text(t, "image")),
                                "rating": self.get_rating_value(rating),
                                "introduction": self.get_intruduction(self.get_text(response_2, "plotSummary")),
                                "id": t["id"]}
                        intro.append(temp)
                        n += 1
        intro = sorted(intro, key=lambda i: i["year"], reverse=True)
        return intro

    def get_top_five_casts(self, id):
        api = ActorApi(self.key)
        query = {"tconst":id[7:16]}
        response = self.do_retrieve(query, "title/get-top-cast")
        length = len(response)
        if length > 5:
            length = 5
        ids = []
        for t in response[0:length]:
            ids.append(t[6:15])
        bio_info = api.get_bio_noname(ids)
        return bio_info

    def get_rating(self, id):
        query = {"tconst":id[7:16]}
        response = self.do_retrieve(query, "title/get-ratings")
        return self.get_text(response, "rating")
