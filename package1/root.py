from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

root = Tk()
root.title('Yummest') #give a name to the window
root.geometry("1200x1000") # set starting size of window
root.minsize(1200, 1000)
root.configure(bg='white')

#build a slider
#vertical = Scale(root, from_=0, to=200)
#vertical.grid()

starter_frame = Frame(root, bg='white').grid(row=10, column=0)
Label(starter_frame, text="   Write your starter choice bellow:", bg="white", fg='black').grid(row=10, column=0, sticky=W, columnspan=2)
starter_log = Image.open('../starter_button.jpg')
starter_log = starter_log.resize((75, 30), Image.ANTIALIAS)
starter_log = ImageTk.PhotoImage(starter_log)
starter_label = Label(starter_frame, image=starter_log).grid(row=11, column=0, sticky=W)
starter_entry = Entry(starter_frame, bd=3)
starter_entry.grid(row=11, column=1, sticky=W)
starter_button = Button(starter_frame, text='Enter').grid(row=11, column=2, sticky=W)


plate_frame = Frame(root, bg='white').grid(row=10, column=3)
Label(plate_frame, text="   Insert a picture of your plate choice:", bg="white", fg='black').grid(row=10, column=3, sticky=W, columnspan=3)
plate_log = Image.open('../plate_button.jpg')
plate_log = plate_log.resize((70, 25), Image.ANTIALIAS)
plate_log = ImageTk.PhotoImage(plate_log)
plate_label = Label(plate_frame, image=plate_log).grid(row=11, column=3, sticky=W)
#Label(plate_frame, text="PLATE", bg="#228B22", fg='#ffffff').grid(row=10, column=3, sticky=W)
plate_entry = Entry(plate_frame, bd=3)
plate_entry.grid(row=11, column=4, sticky=E)

def browse_plate_button():
    file_path = filedialog.askopenfilename(initialdir='/home/almsasantos/Desktop/Ironhack/Final-Project',
                                      title='Please select an image of your desired starter',
                                      filetypes=[('Image Files', ['.jpeg', '.jpg', '.png', '.gif', '.tiff', '.tif', '.bmp'])])
    plate_entry.insert(END, file_path)
    im = Image.open(file_path)
    im = im.resize((128, 128), Image.ANTIALIAS)
    im = ImageTk.PhotoImage(im)
    im_label = Label(image=im)
    im_label.image = im
    im_label.grid(row=12, column=4, sticky=W)

    if not file_path:
        return 'Not image found, please try again!'

plate_button = Button(plate_frame, text='Search', command=browse_plate_button)
plate_button.grid(row=11, column=5, sticky=E)

desert_frame = Frame(root, bg='white').grid(row=10, column=6)
Label(desert_frame, text="   Insert a picture of your desert choice:", bg="white", fg='black').grid(row=10, column=6, sticky=W, columnspan=3)
desert_log = Image.open('../desert_button.jpg')
desert_log= desert_log.resize((75, 30), Image.ANTIALIAS)
desert_log = ImageTk.PhotoImage(desert_log)
desert_label = Label(desert_frame, image=desert_log).grid(row=11, column=6, sticky=W)
#Label(desert_frame, text="DESERT", bg="#228B22", fg='#ffffff').grid(row=10, column=6, sticky=W)
desert_entry = Entry(desert_frame, bd=3)
desert_entry.grid(row=11, column=7, sticky=E)

def browse_desert_button():
    file_path = filedialog.askopenfilename(initialdir='/home/almsasantos/Desktop/Ironhack/Final-Project',
                                      title='Please select an image of your desired starter')
    desert_entry.insert(END, file_path)
    im = Image.open(file_path)
    im = im.resize((128, 128), Image.ANTIALIAS)
    im = ImageTk.PhotoImage(im)
    im_label = Label(image=im)
    im_label.image = im
    im_label.grid(row=12, column=7, sticky=W, rowspan=20, columnspan=20)

    if not file_path:
        return 'Not image found, please try again!'

desert_button = Button(desert_frame, text='Search', command=browse_desert_button)
desert_button.grid(row=11, column=8, sticky=E)

drink_frame = Frame(root, bg='white')
drink_frame.grid(row=10, column=10, rowspan=16)
drink_frame.configure(bg='white')
Label(drink_frame, text="   Select an option bellow:", bg="white", fg='black').grid(row=10, column=9, sticky=W, columnspan=3)
drink_log = Image.open('../drink_button.jpg')
drink_log= drink_log.resize((75, 30), Image.ANTIALIAS)
drink_log= ImageTk.PhotoImage(drink_log)
drink_label = Label(drink_frame, image=drink_log).grid(row=11, column=9, sticky=W)


drink_choice = StringVar()
Radiobutton(drink_frame, text='Copa de vino', variable=drink_choice, value='copa de vino', bg='white').grid(row=11, column=10, sticky=W)
Radiobutton(drink_frame, text='Botella de vino', variable=drink_choice, value='botella de vino', bg='white').grid(row=12, column=10, sticky=W)
Radiobutton(drink_frame, text='Cerveza', variable=drink_choice, value='cerveza', bg='white').grid(row=13, column=10, sticky=W)
Radiobutton(drink_frame, text='Champán', variable=drink_choice, value='champán', bg='white').grid(row=14, column=10, sticky=W)
Radiobutton(drink_frame, text='Agua', variable=drink_choice, value='agua', bg='white').grid(row=15, column=10, sticky=W)
Radiobutton(drink_frame, text='Cocktail', variable=drink_choice, value='cocktail', bg='white').grid(row=16, column=10, sticky=W)
Radiobutton(drink_frame, text='Zumo', variable=drink_choice, value='zumo', bg='white').grid(row=17, column=10, sticky=W)
print(drink_choice.get())

complete = Frame(root)
complete.grid(row=20, column=0, columnspan=20)
completed_button = Button(complete, text='Check The Cheapest Restaurant!')
completed_button.grid(row=30, column=0, padx=50, pady=20)
complete.configure(bg='white')

#upload an image
my_img = Image.open('../img-Recuperado.jpg')
my_img = my_img.resize((1200, 700), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(my_img)
my_img_label = Label(image=my_img)
my_img_label.grid(row=0, column=0, columnspan=15)

#e = Entry(root, width=50, borderwidth=5)
#e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
#e.get() #this function will get whatever is the input
#myButton = Button(root, text='Enter', padx=30)


#Stop programming from working
button_quit = Button(root, text='Exit', command=root.quit)
button_quit.grid(row=32, column=5)

root.mainloop()
