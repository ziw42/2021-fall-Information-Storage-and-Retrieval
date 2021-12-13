import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from functools import partial
from ActorApi import *
import webbrowser
from functools import partial


class ActorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        titleLabel = tk.Label(self, text="Movie Search Engine", font=("Greylock", 50))
        titleLabel.pack(side=tk.TOP, anchor=tk.NW, padx=20, pady=5)

        functionFrame = tk.Frame(self)
        self.controller.values["function"].set(1)
        rb1 = tk.Radiobutton(functionFrame, text="Actor", font=("Calibri", 15),
                             variable=self.controller.values["function"], value=1)
        rb2 = tk.Radiobutton(functionFrame, text="Movie", font=("Calibri", 15),
                             variable=self.controller.values["function"], value=2)
        rb3 = tk.Radiobutton(functionFrame, text="Collaboration", font=("Calibri", 15),
                             variable=self.controller.values["function"], value=3)
        rb1.pack(side=tk.LEFT)
        rb2.pack(side=tk.LEFT, padx=10)
        rb3.pack(side=tk.LEFT, padx=10)
        functionFrame.pack(side=tk.TOP, anchor=tk.NW, padx=20)

        searchLTFrame = tk.Frame(self)
        suggestions = ["Tom Hardy", "Tom Curise", "Tom Holland"]
        queryEntry = AutocompleteCombobox(searchLTFrame, width=40, font=("Calibri", 20),
                                          completevalues=suggestions,
                                          textvariable=self.controller.values["query"])
        queryEntry.pack(side=tk.LEFT)
        searchButton = tk.Button(searchLTFrame, font=("Calibri", 20), text="Search",
                                 height=1, bd=1, command=self.search)

        homeButton = tk.Button(searchLTFrame, font=("Calibri", 20), text="Home", height=1, bd=1,
                               command=self.home)
        homeButton.pack(side=tk.RIGHT)
        searchButton.pack(side=tk.RIGHT, padx=10)
        searchLTFrame.pack(side=tk.TOP, anchor=tk.NW, padx=20)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def update(self):
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.TOP, anchor=tk.NW, padx=20, pady=10, fill=tk.BOTH, expand=1)
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.content = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.infoFrame = tk.Frame(self.content)
        self.infoFrame.pack(side=tk.TOP, anchor=tk.NW)

        if self.controller.values["actor"]["image"] == None:
            self.imageLabel = tk.Label(self.infoFrame, text="No Image", font=("Calibri italic", 25))
        else:
            image = self.urltoImg(self.controller.values["actor"]["image"], 200, 300)
            self.imageLabel = tk.Label(self.infoFrame, image=image)
            self.imageLabel.image = image
        self.imageLabel.pack(side=tk.LEFT, anchor=tk.NW)

        self.name = tk.Label(self.infoFrame, text=self.controller.values["actor"]["name"], font=("Calibri", 30))
        self.name.pack(side=tk.TOP, anchor=tk.NW, padx=10)

        bio_text = self.controller.values["actor"]["introduction"]
        self.bio = tk.Message(self.infoFrame, text=bio_text, font=("Calibri", 20), width=650, justify=tk.LEFT)
        self.bio.pack(side=tk.TOP)

        self.readMore = tk.Button(self.infoFrame, text="Read more on IMDb", font=("Calibri", 15), cursor='hand2', command= lambda: self.openBio(self.controller.values["actor"]["id"]))
        self.readMore.pack(side=tk.RIGHT)

        self.movielistFrame = tk.Frame(self.content)
        self.movielistFrame.pack(side=tk.TOP, anchor=tk.NW)

        self.inMovieLabel = tk.Label(self.movielistFrame, text="Known For", font=("Calibri", 30))
        # self.inMovieLabel.pack(side=TOP, anchor=NW)
        self.inMovieLabel.grid(row=0, column=0)

        movie_list = self.controller.values["actor"]["known_for"]
        row = 1
        for movie in movie_list:
            image = self.urltoImg(movie["image"], 100, 150)
            tempImg = tk.Label(self.movielistFrame, image=image)
            tempImg.image = image
            tempImg.grid(row=row, column=0)

            temp = tk.Label(self.movielistFrame, text=f'{movie["title"]}', font=("Calibri italic", 25), cursor="hand2")
            # temp.pack(side=TOP, anchor=NW)
            temp.bind("<Button-1>", partial(self.openMovie, name=temp.cget('text')))
            temp.grid(row=row, column=1)

            row += 1

        self.recommandFrame = tk.Frame(self.content)
        self.recommandFrame.pack(side=tk.TOP, anchor=tk.NW, pady=10)

        self.recommandLabel = tk.Label(self.recommandFrame, text="See also...", font=("Calibri", 30))
        self.recommandLabel.pack(side=tk.TOP, anchor=tk.NW)

        country = {'USA': 'US', 'UK': 'GB', 'Canada': 'CA', 'France': 'FR', 'Italy': 'IT'}
        home_country = country.get(self.controller.values["actor"]["birthPlace"].split(',')[-1].strip(), 'US')
        self.popular_celebs = self.popular_celeb(home_country)
        self.popularFrame = tk.Frame(self.content)
        self.popularFrame.pack(side=tk.TOP, anchor=tk.NW, pady=10)
        column = 0
        for celeb in self.popular_celebs:
            image = self.urltoImg(celeb["image"], 140, 180)
            tempImg = tk.Label(self.popularFrame, image=image)
            tempImg.image = image
            tempImg.grid(row=0, column=column)

            temp = tk.Label(self.popularFrame, text=f'{celeb["name"]}', font=("Calibri italic", 15), fg="#4169E1", cursor="hand2")
            temp.bind("<Button-1>", partial(self.openActor, name=temp.cget('text')))
            temp.grid(row=1, column=column)

            column += 1

    def urltoImg(self, url, w, h):
        response = requests.get(url)
        image = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((w, h)))
        return image

    def home(self):
        self.frame.destroy()
        self.controller.show_frame("HomePage")

    def search(self):
        self.frame.destroy()
        function = self.controller.values["function"].get()
        if function == 1:
            self.controller.show_frame("ActorSearchPage")
        elif function == 2:
            self.controller.show_frame("FilmSearchPage")
        elif function == 3:
            self.controller.show_frame("CollabSearchPage")

    def openBio(self, id):
        webbrowser.open_new(r"https://www.imdb.com/name/{}/bio".format(id))

    def popular_celeb(self, country):
        return [{'id': 'nm3480246', 'name': 'Ella Purnell', 'image': 'https://m.media-amazon.com/images/M/MV5BMTYxNDk4NDAyMl5BMl5BanBnXkFtZTgwNjIzMTc0NTM@._V1_.jpg'}, {'id': 'nm0267812', 'name': 'Vera Farmiga', 'image': 'https://m.media-amazon.com/images/M/MV5BMjIwNTU3NDUyMl5BMl5BanBnXkFtZTgwODEwODg5NDE@._V1_.jpg'}, {'id': 'nm0717709', 'name': 'Kelly Reilly', 'image': 'https://m.media-amazon.com/images/M/MV5BNjgzMzk2MjEzM15BMl5BanBnXkFtZTgwMTkzMDEwMTE@._V1_.jpg'}, {'id': 'nm2933757', 'name': 'Gal Gadot', 'image': 'https://m.media-amazon.com/images/M/MV5BYThjM2NlOTItYTUzMC00ODE3LTk1MTItM2I3MDViY2U3MThlXkEyXkFqcGdeQXVyMTg4NDI0NDM@._V1_.jpg'}, {'id': 'nm0369513', 'name': 'Cole Hauser', 'image': 'https://m.media-amazon.com/images/M/MV5BZWRiOTdjN2UtY2M1Yy00YzBjLWJmMzQtYTAyZGY4ZGFmZDRkXkEyXkFqcGdeQXVyNDI3NzU1NDE@._V1_.jpg'}]

    def openActor(self, event, name):
        for celeb in self.popular_celebs:
            if celeb['name'] == name:
                id = celeb['id']
                break
        webbrowser.open_new(r"https://www.imdb.com/name/{}".format(id))

    def openMovie(self, event, name):
        for movie in self.controller.values["actor"]["known_for"]:
            if movie["title"] == name:
                id = movie['id']
                break
        webbrowser.open_new(r"https://www.imdb.com{}".format(id))