import numpy as np
import tensorflow
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


food_choices = []
def predict_foods(model_file, type_list_choices, list_of_images, show = True):
    model = load_model(model_file, compile = False)
    for img in list_of_images:
        img = image.load_img(img, target_size=(128, 128))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.

        pred = model.predict(img)
        index = np.argmax(pred)
        type_list_choices.sort()
        pred_value = type_list_choices[index].lower()
        food_choices.append(pred_value)
        if show:
            plt.imshow(img[0])
            plt.axis('off')
            plt.title(pred_value)
            plt.show()


#predict_foods('../models/best_model_9desert.hdf5', ['Apple pie', 'Cannoli', 'Carrot cake', 'Cheesecake', 'Chocolate cake', 'Chocolate mousse', 'Ice cream', 'Strawberry shortcake', 'Tiramisu'], ['../chocolate_cake.jpeg', '../205294.jpg'])


df_initial = pd.read_csv('../data/restaurant_dataframe.csv')
df_initial = df_initial.drop('Unnamed: 0', axis=1)

#since train and test datasets had food names in english we need to translate it to spanish
def translate_food_names(food_list):
    food_dict = {'beef tartare': 'tartar de carne', 'beet salad': 'ensalada', 'breakfast burrito': 'burrito',
                 'caesar salad': 'ensalada', 'caprese salad': 'ensalada',
                 'ceviche': 'ceviche', 'chicken curry': 'curry', 'chicken quesadilla': 'quesadilla',
                 'chicken wings': 'alitas de pollo', 'club sandwich': 'sandwich',
                 'dumplings': 'dumpling', 'edamame': 'edamame', 'falafel': 'falafel',
                 'french fries': 'patatas fritas', 'fried calamari': 'calamares', 'fried rice': 'arroz',
                 'greek salad': 'ensalada', 'guacamole': 'guacamole',
                 'gyoza': 'gyoza', 'hamburger': 'hamburguesa', 'hot dog': 'hot dog',
                 'hummus': 'hummus', 'lasagna': 'lasaña', 'miso soup': 'sopa miso', 'mussels': 'mejillones',
                 'nachos': 'nachos', 'tortilla': 'tortilla', 'onion rings': 'aros de cebolla',
                 'oysters': 'ostras', 'pad thai': 'pad thai', 'paella': 'paella', 'panna cotta': 'panna cotta',
                 'pizza': 'pizza', 'pork chop': 'chuleta', 'prime rib': 'costilla',
                 'ramen': 'ramen', 'ravioli': 'ravioli', 'risotto': 'risotto', 'samosa': 'samosa', 'sashimi': 'sashimi',
                 'scallops': 'vieira', 'seaweed salad': 'ensalada',
                 'spaghetti bolognese': 'boloñesa', 'spaghetti carbonara': 'carbonara',
                 'spring rolls': 'rollito de primavera', 'steak': 'carne',
                 'sushi': 'sushi', 'tacos': 'tacos', 'tuna tartare': 'tartar de atun', 'apple pie': 'tarta de manzana',
                 'cannoli': 'cannoli', 'carrot cake': 'tarta de zanahoria', 'cheesecake': 'tarta de queso',
                 'chocolate cake': 'tarta de chocolate', 'chocolate mousse': 'mouse de chocolate',
                 'ice cream': 'helado', 'strawberry shortcake': 'tarta de fresa', 'tiramisu': 'tiramisu'}
    return [food_dict.get(e,'') for e in food_list]

#plate_choices = translate_food_names(food_choices)

#Calculation of the total of choices:
def cheapest_restaurant():
    df_initial = pd.read_csv('../data/restaurant_dataframe.csv')
    df_initial = df_initial.drop('Unnamed: 0', axis=1)
    prices_df = pd.DataFrame()
    for choice in total_choices_with_drink_and_starter:
        df_product = df_initial.loc[df_initial['product'].str.contains(choice),:]
        prices_df[f'price_{choice}'] = df_product.groupby('restaurant')['price'].min()

    prices_df['total'] = prices_df.sum(axis=1)
    prices_df.dropna(inplace=True)
    prices_df.reset_index(inplace=True)
    prices_df.sort_values(by='total')

    cheapest_restaurant = prices_df['restaurant'][0]
    cheapest_price = prices_df['total'][0]
    print(f'The cheapest restaurant is {cheapest_restaurant}.\n'
          f'The total amount to pay is {cheapest_price}€.')
