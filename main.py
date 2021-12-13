import tkinter as tk
from HomePage import HomePage
from ActorSearchPage import ActorSearchPage
from ActorPage import ActorPage
from CollabSearchPage import CollabSearchPage
from FilmSearchPage import FilmSearchPage
from FilmPage import FilmPage


class MovieSearchEngine(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.values = {"query": tk.StringVar(),
                       "function": tk.IntVar(),
                       "result": [],
                       "actor": {},
                       "film": {}}

        self.frames = {}
        for F in (HomePage, ActorSearchPage, ActorPage, CollabSearchPage, FilmPage, FilmSearchPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name != "HomePage":
            frame.update()
        frame.tkraise()


if __name__ == "__main__":

    start = MovieSearchEngine()
    start.title("Movie Search Engine")
    width = 1000
    height = 800
    screenWidth = start.winfo_screenwidth()
    screenHeight = start.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenWidth - width) / 2, (screenHeight - height) / 2)
    start.geometry(alignstr)
    start.resizable(width=False, height=False)

    start.mainloop()
