from flask import Flask, flash, render_template, redirect, url_for, abort, send_file
from flask import request
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from user_choices import translate_food_names
import pandas as pd
import math
import webbrowser
import requests, json
import os
from PIL import ImageTk, Image
from flask_restful import Api, Resource, reqparse
import random

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    global food_choices, starter_choice_list, plate_choice_list, desert_choice_list, drink_choice_list
    food_choices = []
    if request.method == 'POST':
        starter_choice = request.form['starter'].lower()
        plate_choice = '/home/almsasantos/Desktop/Ironhack/Final-Project/' + request.form['plate']
        desert_choice = '/home/almsasantos/Desktop/Ironhack/Final-Project/' + request.form['desert']
        drink_choice = request.form['drink'].lower()
        starter_choice_list = [starter_choice]
        plate_choice_list = [plate_choice]
        desert_choice_list = [desert_choice]
        drink_choice_list = [drink_choice]
        plate_user_choice()
        desert_user_choice()
        defining_food_choices()
        cheapest_restaurant(total_choices_with_drink_and_starter)
        return redirect('/cheapest_restaurant')
    else:
        return render_template('home.html')

def plate_user_choice():
    if plate_choice_list != ['/home/almsasantos/Desktop/Ironhack/Final-Project/']:
        plates = ['Beef tartare', 'Beet salad', 'Breakfast burrito', 'Caesar salad', 'Caprese salad', 'Ceviche',
                  'Chicken curry', 'Chicken quesadilla', 'Chicken wings', 'Club sandwich',
                  'Dumplings', 'Edamame', 'Falafel', 'French fries', 'Fried calamari', 'Fried rice', 'Greek salad',
                  'Grilled cheese sandwich', 'Guacamole', 'Gyoza', 'Hamburger', 'Hot dog', 'Hummus',
                  'Lasagna', 'Miso soup', 'Mussels', 'Nachos', 'Omelette', 'Onion rings', 'Oysters', 'Pad thai',
                  'Paella', 'Panna cotta', 'Pizza', 'Pork chop', 'Prime rib', 'Ramen',
                  'Ravioli', 'Risotto', 'Samosa', 'Sashimi', 'Seaweed salad', 'Scallops', 'Spaghetti bolognese',
                  'Spaghetti carbonara', 'Spring rolls', 'Steak', 'Sushi', 'Tacos', 'Tuna tartare']
        model_file = '/home/almsasantos/Desktop/Ironhack/Final-Project/Ironhack-Final-Project-Yummest/models/best_model_45class_salads.hdf5'
        model = load_model(model_file, compile=False)
        for img in plate_choice_list:
            img = image.load_img(img, target_size=(128, 128))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img /= 255.

            pred = model.predict(img)
            index = np.argmax(pred)
            plates.sort()
            pred_value = plates[index].lower()
            food_choices.append(pred_value)
    elif plate_choice_list == ['/home/almsasantos/Desktop/Ironhack/Final-Project/']:
        pass

def desert_user_choice():
    if desert_choice_list != ['/home/almsasantos/Desktop/Ironhack/Final-Project/']:
        deserts = ['Apple pie', 'Cannoli', 'Carrot cake', 'Cheesecake', 'Chocolate cake', 'Chocolate mousse',
                   'Ice cream', 'Panna Cotta', 'Strawberry shortcake', 'Tiramisu']
        model_file = '/home/almsasantos/Desktop/Ironhack/Final-Project/Ironhack-Final-Project-Yummest/models/best_model_9desert.hdf5'
        model = load_model(model_file, compile=False)
        for img in desert_choice_list:
            img = image.load_img(img, target_size=(128, 128))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img /= 255.

            pred = model.predict(img)
            index = np.argmax(pred)
            deserts.sort()
            pred_value = deserts[index].lower()
            food_choices.append(pred_value)
    elif desert_choice_list == ['/home/almsasantos/Desktop/Ironhack/Final-Project/']:
        pass

def defining_food_choices():
    global total_choices_with_drink_and_starter
    total_choices = translate_food_names(food_choices)
    if drink_choice_list != ['']:
        total_choices_with_drink_and_starter = total_choices + drink_choice_list
    else:
        total_choices_with_drink_and_starter = total_choices

def cheapest_restaurant(total_choices_with_drink_and_starter):
    global cheapest_restaurant_choice, cheapest_classification, cheapest_price, food_price, not_available, df_initial
    df_initial = pd.read_csv('../data/restaurant_dataframe.csv')
    df_initial = df_initial.drop('Unnamed: 0', axis=1)
    prices_df = pd.DataFrame()
    prices_df_product = pd.DataFrame()
    prices_df_merge = pd.DataFrame()
    food_price = {}
    not_available = []

    if starter_choice_list == ['']:
        for choice in total_choices_with_drink_and_starter:
            # self.df_product_initial = self.df_initial.loc[self.df_initial['type'].str.contains(['plato', 'bebida']), :]
            df_product = df_initial.loc[df_initial['product'].str.contains(choice), :]
            prices_df[f'price_{choice}'] = df_product.groupby('restaurant')['price'].min()

        if 0 not in list(prices_df.isnull().sum(axis=1)):
            prices_df.dropna(thresh=len(total_choices_with_drink_and_starter) - 1, axis=0, inplace=True)
            prices_df['total'] = prices_df.sum(axis=1)
            prices_df.sort_values(by='total', inplace=True)
            prices_df.reset_index(inplace=True)
            print(prices_df)

        else:
            prices_df['total'] = prices_df.sum(axis=1)
            prices_df.dropna(inplace=True)
            prices_df.sort_values(by='total', inplace=True)
            prices_df.reset_index(inplace=True)

        cheapest_restaurant_choice = prices_df['restaurant'][0].upper()
        cheapest_price = prices_df['total'][0]
        cheapest_classification = list(df_initial[df_initial['restaurant'] == cheapest_restaurant_choice.lower()]['rating'].sort_values())[0]

        for col in prices_df.columns:
            if col == 'index' or col == 'restaurant' or col == 'total' or col == 'level_0':
                pass
            else:
                if math.isnan(prices_df[col][0]):
                    not_available.append(col.replace('price_', ''))
                else:
                    food_price[col.replace('price_', '')] = prices_df[col][0]

    else:
        df_starter = df_initial.loc[df_initial['type'].str.contains('entrante'), :]
        df_starter_choice = df_starter.loc[df_starter['product'].str.contains(starter_choice_list[0]), :]
        prices_df[f'price_{starter_choice_list[0]}'] = df_starter_choice.groupby('restaurant')['price'].min()
        prices_df.reset_index(inplace=True)
        print(prices_df)

        for choice in total_choices_with_drink_and_starter:
            df_product = df_initial.loc[df_initial['product'].str.contains(choice), :]
            prices_df_product[f'price_{choice}'] = df_product.groupby('restaurant')['price'].min()
        prices_df_product.reset_index(inplace=True)
        print(prices_df_product)

        prices_df_merge = pd.merge(left=prices_df, right=prices_df_product, left_index=False, right_index=False)
        prices_df_merge.reset_index(drop=True)
        print(prices_df_merge)

        if prices_df_merge.empty == True:
            prices_df_merge = pd.concat([prices_df, prices_df_product]).reset_index(drop=True)

        if 0 not in list(prices_df_merge.isnull().sum(axis=1)):
            prices_df_merge.dropna(thresh=len(total_choices_with_drink_and_starter + starter_choice_list) - 1,axis=0, inplace=True)
            prices_df_merge['total'] = prices_df_merge.sum(axis=1)
            prices_df_merge.sort_values(by='total', inplace=True)
            prices_df_merge.reset_index(inplace=True)

        else:
            prices_df_merge.dropna(inplace=True)
            prices_df_merge['total'] = prices_df_merge.sum(axis=1)
            prices_df_merge.sort_values(by='total', inplace=True)
            prices_df_merge.reset_index(inplace=True)
            print(prices_df_merge)

        cheapest_restaurant_choice = prices_df_merge['restaurant'][0].upper()
        print(cheapest_restaurant_choice)
        cheapest_price = prices_df_merge['total'][0]
        print(cheapest_price)
        cheapest_classification = list(df_initial[df_initial['restaurant'] == cheapest_restaurant_choice.lower()]['rating'].sort_values())[0]
        print(cheapest_classification)

        for col in prices_df_merge.columns:
            if col == 'index' or col == 'restaurant' or col == 'total' or col == 'level_0':
                pass
            else:
                if math.isnan(prices_df_merge[col][0]):
                    not_available.append(col.replace('price_', ''))
                else:
                    food_price[col.replace('price_', '')] = prices_df_merge[col][0]

@app.route('/cheapest_restaurant', methods=["POST", "GET"])
def rest_price():
    #self.defining_food_choices()
    cheapest_words = [cheapest_restaurant_choice, cheapest_classification, round(cheapest_price,2)]
    if cheapest_classification == 'none':
        return render_template('plates_no_class.html', data=cheapest_words)
    else:
        return render_template('plates.html', data=cheapest_words)

@app.route('/tourist_attractions', methods=["POST", "GET"])
def pop_map():
    global madrid_lat_long
    global open_maps_browser
    cheapest_lat_log = df_initial[df_initial['restaurant'] == cheapest_restaurant_choice.lower()].reset_index()
    cheapest_lat = cheapest_lat_log['lat'][0]
    cheapest_log = cheapest_lat_log['log'][0]
    madrid_lat_long = [cheapest_lat, cheapest_log]
    ROUTE = f'https://www.google.com/maps/dir/40.3923994,-3.6987236/{cheapest_lat},{cheapest_log}'
    print(ROUTE)
    open_maps_browser = webbrowser.open_new(ROUTE)
    venue_suggestion()
    return render_template('/tourist_attractions.html', total_venues=total_venues)

def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']

    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

def getDfFoursquareNearbyVenues(limit=500, radius=1000):
    lat = madrid_lat_long[0]
    lng = madrid_lat_long[1]
    url = 'https://api.foursquare.com/v2/venues/explore'
    params = dict(client_id='',
                  client_secret='',
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
        nearby_venues['venue.categories'] = nearby_venues.apply(get_category_type, axis=1)
        # clean columns
        nearby_venues.columns = [col.split(".")[-1] for col in nearby_venues.columns]
        return nearby_venues

def venue_suggestion():
    # venues near the restaurant lat-long defined:
    global total_venues
    total_venues = []
    df_venues = getDfFoursquareNearbyVenues()
    venue_options = ['Plaza', 'Art Museum', 'Monument / Landmark', 'Art Gallery', 'Church', 'Palace', 'Opera House',
                         'Historic Site', 'Theater', 'Movie Theater', 'Indie Movie Theater', 'Garden']
    df_venue_options = df_venues[df_venues['categories'].isin(venue_options)].reset_index()
    if len(df_venue_options) > 2:
        two_options_venue = f"Nearby you can visit a {df_venue_options['categories'][0].upper()} called {df_venue_options['name'][0]} and a {df_venue_options['categories'][1].upper()} called {df_venue_options['name'][1]}!"
        total_venues.append(two_options_venue)
    elif len(df_venue_options) > 1:
        one_options_venue = f"Nearby you can visit a {df_venue_options['categories'][0].upper()} called {df_venue_options['name'][0]}!"
        total_venues.append(one_options_venue)
    else:
        no_options_venue = 'There is no tourist attraction available.'
        total_venues.append(no_options_venue)
    print(total_venues)

if __name__ == '__main__':
    app.run(debug=True)