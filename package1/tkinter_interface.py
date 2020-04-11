from tkinter import *
import numpy as np
import pandas as pd
from PIL import ImageTk, Image
from tkinter import filedialog
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from user_choices import translate_food_names
from tkinter import messagebox
import webbrowser
import math
import requests, json
from bs4 import BeautifulSoup
from pandas.io.json import json_normalize


class App(Frame):
    def __init__(self, master):
        self.master = master
        self.master.title('Yummest')
        self.master.geometry("1200x1000")  # set starting size of window
        self.master.minsize(1200, 1000)
        self.master.configure(bg='white')


        # upload the bender image
        self.load = Image.open('../../img-Recuperado.jpg').resize((1200, 700), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self.master, image=self.render)
        self.img.grid(row=0, column=0, columnspan=15)


        #Everything about starters:
        self.starter_choice = StringVar()
        self.starter_frame = Frame(self.master, bg='white')
        self.starter_frame.grid(row=10, column=0)
        self.starter_label = Label(self.starter_frame, text="   Write your starter choice bellow:", bg="white", fg='black')
        self.starter_label.grid(row=10, column=0, sticky=W, columnspan=2)
        self.starter_load = Image.open('../../starter_button.jpg').resize((75, 30), Image.ANTIALIAS)
        self.starter_render = ImageTk.PhotoImage(self.starter_load)
        self.starter_label_ = Label(self.starter_frame, image=self.starter_render)
        self.starter_label_.grid(row=11, column=0, sticky=W)
        self.starter_entry = Entry(self.starter_frame, bd=3, textvariable=self.starter_choice)
        self.starter_entry.grid(row=11, column=1, sticky=W)
        self.starter_button = Button(self.starter_frame, text='Enter', command=self.get_starter_choice)
        self.starter_button.grid(row=11, column=2, sticky=W)


        #Everything about plates:
        self.plate_choice=StringVar()
        self.plate_frame = Frame(self.master, bg='white')
        self.plate_frame.grid(row=10, column=3)
        self.plate_label = Label(self.plate_frame, text="   Insert a picture of your plate choice:", bg="white", fg='black')
        self.plate_label.grid(row=10, column=3, sticky=W, columnspan=3)
        self.plate_load = Image.open('../../plate_button.jpg').resize((70, 25), Image.ANTIALIAS)
        self.plate_render = ImageTk.PhotoImage(self.plate_load)
        self.plate_label_ = Label(self.plate_frame, image=self.plate_render)
        self.plate_label_.grid(row=11, column=3, sticky=W)
        self.plate_entry = Entry(self.plate_frame, bd=3, textvariable=self.plate_choice)
        self.plate_entry.grid(row=11, column=4, sticky=E)
        self.plate_button = Button(self.plate_frame, text='Search', command=self.browse_plate_button)
        self.plate_button.grid(row=11, column=5, sticky=E)

        #Everything about deserts:
        self.desert_choice = StringVar()
        self.desert_frame = Frame(self.master, bg='white')
        self.desert_frame.grid(row=10, column=6)
        self.desert_label = Label(self.desert_frame, text="   Insert a picture of your desert choice:", bg="white", fg='black')
        self.desert_label.grid(row=10, column=6, sticky=W, columnspan=3)
        self.desert_load = Image.open('../../desert_button.jpg').resize((75, 30), Image.ANTIALIAS)
        self.desert_render = ImageTk.PhotoImage(self.desert_load)
        self.desert_label_ = Label(self.desert_frame, image=self.desert_render)
        self.desert_label_.grid(row=11, column=6, sticky=W)
        self.desert_entry = Entry(self.desert_frame, bd=3, textvariable=self.desert_choice)
        self.desert_entry.grid(row=11, column=7, sticky=E)
        self.desert_button = Button(self.desert_frame, text='Search', command=self.browse_desert_button)
        self.desert_button.grid(row=11, column=8, sticky=E)

        #Everything about drinks:
        self.drink_choice = StringVar()
        self.drink_frame = Frame(self.master, bg='white')
        self.drink_frame.grid(row=10, column=10, rowspan=16)
        self.drink_frame.configure(bg='white')
        self.drink_label= Label(self.drink_frame, text="   Select an option bellow:", bg="white", fg='black')
        self.drink_label.grid(row=10, column=9, sticky=W, columnspan=3)
        self.drink_load = Image.open('../../drink_button.jpg').resize((75, 30), Image.ANTIALIAS)
        self.drink_render = ImageTk.PhotoImage(self.drink_load)
        self.drink_label_ = Label(self.drink_frame, image=self.drink_render)
        self.drink_label_.grid(row=11, column=9, sticky=W)

        Radiobutton(self.drink_frame, text='Copa de vino', variable=self.drink_choice, value='copa de vino', bg='white').grid(row=11, column=10, sticky=W)
        Radiobutton(self.drink_frame, text='Botella de vino', variable=self.drink_choice, value='botella de vino', bg='white').grid(row=12, column=10, sticky=W)
        Radiobutton(self.drink_frame, text='Cerveza', variable=self.drink_choice, value='cerveza', bg='white').grid(row=13, column=10, sticky=W)
        Radiobutton(self.drink_frame, text='Champán', variable=self.drink_choice, value='champan', bg='white').grid(row=14, column=10, sticky=W)
        Radiobutton(self.drink_frame, text='Agua', variable=self.drink_choice, value='agua', bg='white').grid(row=15, column=10, sticky=W)
        Radiobutton(self.drink_frame, text='Cocktail', variable=self.drink_choice, value='cocktail', bg='white').grid(row=16, column=10, sticky=W)
        Radiobutton(self.drink_frame, text='Zumo', variable=self.drink_choice, value='zumo', bg='white').grid(row=17, column=10, sticky=W)

        #Once you have all your choices:
        self.complete = Frame(self.master)
        self.complete.grid(row=50, column=2, columnspan=5)
        self.completed_button = Button(self.complete, text='Check The Cheapest Restaurant', compound='top' , command= self.complete_button_func)
        self.completed_button.grid(row=50, column=0, columnspan=10, padx=50, pady=20)
        self.complete.configure(bg='white')

        # Once you have all your choices:
        self.map = Frame(self.master)
        self.map.grid(row=51, column=1, columnspan=5)
        self.map_button = Button(self.map, text='Check the direction', command=self.pop_map)
        self.map_button.grid(row=51, column=0, columnspan=10, padx=20, pady=20)
        self.map.configure(bg='white')

        # Venues suggestions:
        self.venue = Frame(self.master)
        self.venue.grid(row=51, column=4, columnspan=5)
        self.venue_button = Button(self.venue, text='Check tourist attraction', command=self.venue_suggestion)
        self.venue_button.grid(row=51, column=0, columnspan=10, padx=20, pady=20)
        self.venue.configure(bg='white')

        self.food_choices = []
        self.df_initial = pd.read_csv('../data/restaurant_dataframe.csv')

    def browse_plate_button(self):
        file_path = filedialog.askopenfilename(initialdir='/home/almsasantos/Desktop/Ironhack/Final-Project',
                                          title='Please select an image of your desired starter')
        self.plate_entry.insert(END, file_path)
        self.im_load = Image.open(file_path).resize((128, 128), Image.ANTIALIAS)
        self.im_render = ImageTk.PhotoImage(self.im_load)
        self.im_label = Label(image=self.im_render)
        self.im_label.image = self.im_render
        self.im_label.grid(row=12, column=3, rowspan=30)

    def get_starter_choice(self):
        if self.starter_choice.get() != '':
            self.df_initial_starter = pd.read_csv('../data/restaurant_dataframe.csv')
            df_starter = self.df_initial_starter.loc[self.df_initial_starter['type'].str.contains('entrante'), :]
            if df_starter.loc[df_starter['product'].str.contains(self.starter_choice.get()),:].empty == True:
                return messagebox.showerror(title='Starter option error', message=f"{self.starter_choice.get()} isn't available, try again.")
            else:
                starter = [self.starter_choice.get()]
                return starter

    def get_plate_choice(self):
        plate = [self.plate_choice.get()]
        return plate

    def get_desert_choice(self):
        desert = [self.desert_choice.get()]
        return desert

    def get_drink_choice(self):
        drink = [self.drink_choice.get()]
        return drink

    def browse_desert_button(self):
        file_path = filedialog.askopenfilename(initialdir='/home/almsasantos/Desktop/Ironhack/Final-Project',
                                               title='Please select an image of your desired starter')
        self.desert_entry.insert(END, file_path)
        self.im_load = Image.open(file_path).resize((128, 128), Image.ANTIALIAS)
        self.im_render = ImageTk.PhotoImage(self.im_load)
        self.im_label = Label(image=self.im_render)
        self.im_label.image = self.im_render
        self.im_label.grid(row=12, column=6, rowspan=30)

    def predict_foods(self, model_file, type_list_choices, list_of_images):
        global food_choices
        self.model = load_model(model_file, compile = False)
        for img in list_of_images:
            img = image.load_img(img, target_size=(128, 128))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img /= 255.

            pred = self.model.predict(img)
            index = np.argmax(pred)
            type_list_choices.sort()
            self.pred_value = type_list_choices[index].lower()
            self.food_choices.append(self.pred_value)

    def cheapest_restaurant(self, total_choices_with_drink_and_starter):
        global cheapest_restaurant_choice
        global cheapest_classification
        global cheapest_price
        global food_price
        global not_available
        self.df_initial = pd.read_csv('../data/restaurant_dataframe.csv')
        self.df_initial = self.df_initial.drop('Unnamed: 0', axis=1)
        self.prices_df = pd.DataFrame()
        self.prices_df_product = pd.DataFrame()
        self.prices_df_merge = pd.DataFrame()
        self.food_price = {}
        self.not_available = []

        if self.starter_guay == None:
            for choice in total_choices_with_drink_and_starter:
                #self.df_product_initial = self.df_initial.loc[self.df_initial['type'].str.contains(['plato', 'bebida']), :]
                df_product = self.df_initial.loc[self.df_initial['product'].str.contains(choice), :]
                self.prices_df[f'price_{choice}'] = df_product.groupby('restaurant')['price'].min()

            if 0 not in list(self.prices_df.isnull().sum(axis=1)):
                self.prices_df.dropna(thresh=len(total_choices_with_drink_and_starter)-1, axis=0, inplace=True)
                self.prices_df['total'] = self.prices_df.sum(axis=1)
                self.prices_df.sort_values(by='total', inplace=True)
                self.prices_df.reset_index(inplace=True)
                print(self.prices_df)

            else:
                self.prices_df['total'] = self.prices_df.sum(axis=1)
                self.prices_df.dropna(inplace=True)
                self.prices_df.sort_values(by='total', inplace=True)
                self.prices_df.reset_index(inplace=True)

            self.cheapest_restaurant_choice = self.prices_df['restaurant'][0].upper()
            self.cheapest_price = self.prices_df['total'][0]
            self.cheapest_classification = list(self.df_initial[self.df_initial['restaurant'] == self.cheapest_restaurant_choice.lower()]['rating'].sort_values())[0]

            for col in self.prices_df.columns:
                if col == 'index' or col == 'restaurant' or col == 'total' or col == 'level_0':
                    pass
                else:
                    if math.isnan(self.prices_df[col][0]):
                        self.not_available.append(col.replace('price_', ''))
                    else:
                        self.food_price[col.replace('price_', '')] = self.prices_df[col][0]

        else:
            self.df_starter = self.df_initial.loc[self.df_initial['type'].str.contains('entrante'), :]
            self.df_starter_choice = self.df_starter.loc[self.df_starter['product'].str.contains(self.starter_guay[0]), :]
            self.prices_df[f'price_{self.starter_guay[0]}'] = self.df_starter_choice.groupby('restaurant')['price'].min()
            self.prices_df.reset_index(inplace=True)
            print(self.prices_df)

            for choice in total_choices_with_drink_and_starter:
                df_product = self.df_initial.loc[self.df_initial['product'].str.contains(choice), :]
                self.prices_df_product[f'price_{choice}'] = df_product.groupby('restaurant')['price'].min()
            self.prices_df_product.reset_index(inplace=True)
            print(self.prices_df_product)

            self.prices_df_merge = pd.merge(left=self.prices_df, right=self.prices_df_product, left_index=False, right_index=False)
            self.prices_df_merge.reset_index(drop=True)

            if self.prices_df_merge.empty == True:
                self.prices_df_merge = pd.concat([self.prices_df, self.prices_df_product]).reset_index(drop=True)

            if 0 not in list(self.prices_df_merge.isnull().sum(axis=1)):
                self.prices_df_merge.dropna(thresh=len(total_choices_with_drink_and_starter+self.starter_guay)-1, axis=0, inplace=True)
                self.prices_df_merge['total'] = self.prices_df_merge.sum(axis=1)
                self.prices_df_merge.sort_values(by='total', inplace=True)
                self.prices_df_merge.reset_index(inplace=True)

            else:
                self.prices_df_merge.dropna(inplace=True)
                self.prices_df_merge['total'] = self.prices_df_merge.sum(axis=1)
                self.prices_df_merge.sort_values(by='total', inplace=True)
                self.prices_df_merge.reset_index(inplace=True)

            self.cheapest_restaurant_choice = self.prices_df_merge['restaurant'][0].upper()
            self.cheapest_price = self.prices_df_merge['total'][0]
            self.cheapest_classification = list(self.df_initial[self.df_initial['restaurant'] == self.cheapest_restaurant_choice.lower()]['rating'].sort_values())[0]

            for col in self.prices_df_merge.columns:
                if col == 'index' or col == 'restaurant' or col == 'total' or col == 'level_0':
                    pass
                else:
                    if math.isnan(self.prices_df_merge[col][0]):
                        self.not_available.append(col.replace('price_', ''))
                    else:
                        self.food_price[col.replace('price_', '')] = self.prices_df_merge[col][0]


    def complete_button_func(self):
        self.resume_choice()
        self.rest_price()

    def resume_choice(self):
        self.defining_food_choices()
        food_dict = self.food_price
        self.show_food = []
        for k, v in food_dict.items():
            self.show_food.append(f'The price of {k.upper()} is {v}€.')
        for n in self.not_available:
            self.show_food.append(f'The {n} is not available.')
        self.show_food = "\n".join(self.show_food)
        return messagebox.showinfo('Resume of your food choices', self.show_food)

    def rest_price(self):
        #self.defining_food_choices()
        if self.cheapest_classification == 'none':
            return messagebox.showinfo("Restaurant to go:", f'The cheapest restaurant is {self.cheapest_restaurant_choice}.\nThe total amount to pay is {self.cheapest_price:.2f}€.')
        else:
            return messagebox.showinfo("Restaurant to go:", f'The cheapest restaurant is {self.cheapest_restaurant_choice} with a classification of {self.cheapest_classification}.\nThe total amount to pay is {self.cheapest_price:.2f}€.')

    def defining_food_choices(self):
        global starter_guay
        global drink_guay
        self.starter_guay = self.get_starter_choice()
        if self.get_plate_choice() != ['']:
            plates = ['Beef tartare', 'Beet salad', 'Breakfast burrito', 'Caesar salad', 'Caprese salad', 'Ceviche', 'Chicken curry', 'Chicken quesadilla', 'Chicken wings', 'Club sandwich',
                      'Dumplings', 'Edamame', 'Falafel', 'French fries', 'Fried calamari', 'Fried rice', 'Greek salad', 'Grilled cheese sandwich', 'Guacamole', 'Gyoza', 'Hamburger', 'Hot dog', 'Hummus',
                      'Lasagna', 'Miso soup', 'Mussels', 'Nachos', 'Omelette', 'Onion rings', 'Oysters', 'Pad thai', 'Paella', 'Panna cotta', 'Pizza', 'Pork chop', 'Prime rib', 'Ramen',
                      'Ravioli', 'Risotto', 'Samosa', 'Sashimi', 'Seaweed salad', 'Scallops', 'Spaghetti bolognese', 'Spaghetti carbonara', 'Spring rolls', 'Steak', 'Sushi', 'Tacos', 'Tuna tartare']
            self.predict_foods(model_file='/home/almsasantos/Desktop/Ironhack/Final-Project/Ironhack-Final-Project-Yummest/models/best_model_45class_salads.hdf5', type_list_choices=plates, list_of_images=self.get_plate_choice())

        if self.get_desert_choice() != ['']:
            deserts = ['Apple pie', 'Cannoli', 'Carrot cake', 'Cheesecake', 'Chocolate cake', 'Chocolate mousse',
                       'Ice cream', 'Panna Cotta', 'Strawberry shortcake', 'Tiramisu']
            self.predict_foods(model_file='/home/almsasantos/Desktop/Ironhack/Final-Project/Ironhack-Final-Project-Yummest/models/best_model_9desert.hdf5', type_list_choices=deserts, list_of_images=self.get_desert_choice())

        # following line of code is to translate the training plates model into spanish plates:
        self.total_choices = translate_food_names(self.food_choices)

        drink_guay = self.get_drink_choice()
        if drink_guay !=['']:
            self.total_choices_with_drink_and_starter = self.total_choices + self.get_drink_choice()
        else:
            self.total_choices_with_drink_and_starter = self.total_choices

        self.cheapest_restaurant(self.total_choices_with_drink_and_starter)

    def pop_map(self):
        global madrid_lat_long
        self.cheapest_lat_log = self.df_initial[self.df_initial['restaurant'] == self.cheapest_restaurant_choice.lower()].reset_index()
        self.cheapest_lat = self.cheapest_lat_log['lat'][0]
        self.cheapest_log = self.cheapest_lat_log['log'][0]
        self.madrid_lat_long = [self.cheapest_lat, self.cheapest_log]
        ROUTE = f'https://www.google.com/maps/dir/40.3923994,-3.6987236/{self.cheapest_lat},{self.cheapest_log}'
        webbrowser.open_new(ROUTE)

    def get_category_type(self, row):
        try:
            categories_list = row['categories']
        except:
            categories_list = row['venue.categories']

        if len(categories_list) == 0:
            return None
        else:
            return categories_list[0]['name']

    def getDfFoursquareNearbyVenues(self, limit=500, radius=1000):
        lat = self.madrid_lat_long[0]
        lng = self.madrid_lat_long[1]
        url = 'https://api.foursquare.com/v2/venues/explore'
        params = dict(
            client_id='',
            client_secret='L',
            v='',
            ll='%s,%s' % (lat, lng),
            radius='%s' % (radius),
            limit=limit)
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        venues = data['response']['groups'][0]['items']
        nearby_venues = pd.json_normalize(venues)  # flatten JSON
        print('Found %s nearby venues at %s,%s' % (len(nearby_venues.index), lat, lng))

        # filter columns
        filtered_columns = ['venue.name', 'venue.categories', 'venue.location.lat', 'venue.location.lng']
        if (len(nearby_venues.index) > 0):
            nearby_venues = nearby_venues.loc[:, filtered_columns]
            # filter the category for each row
            nearby_venues['venue.categories'] = nearby_venues.apply(self.get_category_type, axis=1)
            # clean columns
            nearby_venues.columns = [col.split(".")[-1] for col in nearby_venues.columns]
        return nearby_venues

    def venue_suggestion(self):
        # venues near the restaurant lat-long defined:
        df_venues = self.getDfFoursquareNearbyVenues()
        venue_options = ['Plaza', 'Art Museum', 'Monument / Landmark', 'Art Gallery', 'Church', 'Palace', 'Opera House',
                         'Historic Site', 'Theater', 'Movie Theater', 'Indie Movie Theater', 'Garden']
        self.df_venue_options = df_venues[df_venues['categories'].isin(venue_options)].reset_index()
        if len(self.df_venue_options) > 2:
            return messagebox.showinfo('Suggestion:',
                                       f"Nearby you can visit a {self.df_venue_options['categories'][0].upper()} called {self.df_venue_options['name'][0]} "
                                       f"and a {self.df_venue_options['categories'][1].upper()} called {self.df_venue_options['name'][1]}!")
        elif len(self.df_venue_options) > 1:
            return messagebox.showinfo('Suggestion:',
                                       f"Nearby you can visit a {self.df_venue_options['categories'][0].upper()} called {self.df_venue_options['name'][0]}!")
        else:
            return messagebox.showinfo('Suggestion:', 'There is no tourist attraction available.')


def main():
    root=Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
