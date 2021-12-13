import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        titleLabel = tk.Label(self, text="Movie Search Engine", font=("Greylock", 100))
        titleLabel.place(relx=.5, rely=.4, anchor="center")

        functionFrame = tk.Frame(self)
        self.controller.values["function"].set(1)
        rb1 = tk.Radiobutton(functionFrame, text="Actor", font=("Calibri", 20),
                             variable=self.controller.values["function"], value=1)
        rb2 = tk.Radiobutton(functionFrame, text="Movie", font=("Calibri", 20),
                             variable=self.controller.values["function"], value=2)
        rb3 = tk.Radiobutton(functionFrame, text="Collaboration", font=("Calibri", 20),
                             variable=self.controller.values["function"], value=3)
        rb1.pack(side=tk.LEFT)
        rb2.pack(side=tk.LEFT, padx=10)
        rb3.pack(side=tk.LEFT, padx=10)
        functionFrame.place(relx=0.5, rely=0.55, anchor="center")

        searchFrame = tk.Frame(self)

        suggestions = ["Tom Hardy", "Tom Cruise", "Tom Holland"]
        queryEntry = AutocompleteCombobox(searchFrame, width=40, font=("Calibri", 25),
                                          completevalues=suggestions,
                                          textvariable=self.controller.values["query"])
        queryEntry.pack(side=tk.LEFT)
        # self.queryEntry.bind("<Button-1>", self.clear_search)
        searchButton = tk.Button(searchFrame, font=("Calibri", 25), text="Search", height=1, bd=1,
                                 command=self.search)
        searchButton.pack(side=tk.RIGHT, padx=10)
        searchFrame.place(relx=.5, rely=.63, anchor="center")

    def search(self):
        function = self.controller.values["function"].get()
        if function == 1:
            self.controller.show_frame("ActorSearchPage")
        elif function == 2:
            self.controller.show_frame("FilmSearchPage")
        elif function == 3:
            self.controller.show_frame("CollabSearchPage")
