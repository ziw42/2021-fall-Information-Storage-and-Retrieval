import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from functools import partial
from ActorApi import *
from CollaborationApi import *
import ApiKey
import webbrowser


class CollabSearchPage(tk.Frame):

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


    def urltoImg(self, url, w, h):
        response = requests.get(url)
        image = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((w, h)))
        return image

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

        # self.outcomeFrame = tk.Frame(self.content)
        # self.outcomeFrame.pack(side=tk.TOP, anchor=tk.NW)

        self.outcomeLabel = tk.Label(self.content, text="Search Results", font=("Calibri", 30))
        self.outcomeLabel.grid(row=0, column=0)

        #key = "d059029339msh401f1d3ff774d0cp13c27ejsn70e16e2f94b2"
        key = ApiKey.give_key()
        collab = CollaborationApi(key)
        self.result = collab.get_collaboration(self.controller.values["query"].get())

        row = 1
        for title, url in self.result.items():
            img = url.split(',')[0]
            image = self.urltoImg(img, 200, 300)
            tempImg = tk.Label(self.content, image=image)
            tempImg.image = image
            tempImg.grid(row=row, column=0)
            temp = tk.Button(self.content, text=f'{title}', font=("Calibri italic", 25), cursor="hand2")
            temp.bind("<Button-1>", partial(self.openMovie, name=temp.cget('text')))
            temp.grid(row=row, column=1)
            row += 1

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

    def openMovie(self, event, name):
        for title, url in self.result.items():
            if title == name:
                id = url.split(',')[1]
                break
        webbrowser.open_new(r"https://www.imdb.com{}".format(id))