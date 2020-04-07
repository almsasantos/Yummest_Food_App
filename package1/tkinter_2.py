from tkinter import *
from PIL import ImageTk, Image
import webbrowser

class GoogleMaps(Frame):
    def __init__(self, master, im):
        Frame.__init__(self, master)
        self.caption = Label(self, text="Some text about the map")
        self.caption.grid()
        self.image = ImageTk.PhotoImage(im)  # <--- results of PhotoImage() must be stored
        self.image_label = Label(self, image=self.image, bd=0)  # <--- will not work if 'image = ImageTk.PhotoImage(im)'

        self.image_label.grid()
        self.grid()

im = webbrowser.open("test.html") # read map from disk

def main():
    # or you could use the PIL image you created directly via option 2 from the URL request ...
    mainw = Tk()
    mainw.frame = GoogleMaps(mainw, im)
    mainw.mainloop()

if __name__ == '__main__':
    main()
