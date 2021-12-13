import requests

class ActorApi:
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

    def get_minibios(self, minibios):
        if minibios is not None:
            return minibios[0]["text"]
        else:
            return None

    def get_known_for(self, id):
        query = {"nconst": id}
        response = self.do_retrieve(query, "actors/get-known-for")
        known_for = []
        for t in response:
            temp = {}
            temp["title"] = self.get_text(t["title"], "title")
            temp["id"] = self.get_text(t["title"], "id")
            temp["image"] = self.get_image_url(self.get_text(t["title"], "image"))
            known_for.append(temp)
        return known_for


    def get_bio_noname(self, ids):
        biolist = []
        if ids is not None:
            for t in ids:
                print(t)
                if "nm" in t:
                    query = {"nconst": t}
                    response = self.do_retrieve(query, "actors/get-bio")
                    full_intruduction = self.get_minibios(self.get_text(response, "miniBios"))
                    if full_intruduction is not None:
                        introduction = full_intruduction.split("\n")[0] + " ..."
                    else:
                        introduction = None
                    temp = {"id": t, "name": self.get_text(response, "name"), "birthDate": self.get_text(response, "birthDate"),
                            "gender": self.get_text(response, "gender"),
                            "height": self.get_text(response, "heightCentimeters"),
                            "fullName": self.get_text(response, "realName"),
                            "image": self.get_image_url(self.get_text(response, "image")),
                            "akas": self.get_text(response, "akas"), "nicknames": self.get_text(response, "nicknames"),
                            "birthPlace": self.get_text(response, "birthPlace"),
                            "spouses": self.get_text(response, "spouses"),
                            "trademarks": self.get_text(response, "trademarks"),
                            "introduction": introduction, "full_intruduction": full_intruduction,
                            "known_for": self.get_known_for(t)}
                    biolist.append(temp)
        return biolist

    def get_bio(self, name):
        return self.get_bio_noname(self.get_id(name))
