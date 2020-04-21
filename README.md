<img src='https://scontent.flis5-1.fna.fbcdn.net/v/t1.15752-9/92339357_220548049017845_6393812114410045440_n.jpg?_nc_cat=109&_nc_sid=b96e70&_nc_ohc=Wtzo8ySz9AkAX88xMgv&_nc_ht=scontent.flis5-1.fna&oh=9a6af59c3b491b9e9c2310f4d38aff61&oe=5EADB47C' width="100" height="100">

# Yummest

#### Ana Santos - Final Project - Data Analytics Bootcamp - Ironhack Madrid

## Goal
The goal of **Yummest** is to help you find the **restaurant** where your **entire meal** chosen is the **cheapest** by passing photos of your plate and desert to the app. 

## Overview
Let's imagine you're traveling in a foreign country meanwhile you want to eat out in a restaurant but you don't want to spend a lot of money by going to a tourist's restaurant and don't know how to speak its language. The tool needed in these cases is an app that allows you to search the food you wanna eat based on photos.

Yummest receives individual **pictures** of each **plate and desert**, and a **text** of your **starter and drink**. Based on that information provides you the direction to the restaurant where that full meal is cheaper and gives you suggestions of other tourist attractions nearby that you can visit as well.

## Data
* [El tenedor](https://www.eltenedor.es/)

Data from ***El Tenedor*** website was used to make estimations of the cheapest meal, using each menu available in each restaurant of Madrid.

* [Food-101 dataset](https://www.kaggle.com/dansbecker/food-101)

***Food-101 dataset** of **Kaggle*** was used to get the images ready to train the neural network to predict each category of plate and desert.

* [Foursquare](https://foursquare.com)

The ***Foursquare API*** was used to make suggestions of tourist attractions that people can visit nearby the cheapest restaurant.

## Methodology

1. **Web-scraping of *El Tenedor*'s web page** to get all the prices of every plate of the menu of each restaurant in Madrid, and its classification, latitud and longitud.
![df_initial](https://scontent.flis5-1.fna.fbcdn.net/v/t1.15752-9/94158380_877745969358660_8281810988190138368_n.png?_nc_cat=110&_nc_sid=b96e70&_nc_ohc=YMaT7V92jAkAX9O734U&_nc_ht=scontent.flis5-1.fna&oh=0f41b511df0eba321d35deacc76c8e57&oe=5EC2CE3C#center)


2. **Image Classification**: Train a model by using *InceptionV3* of **Keras**. For that purpose, each food category was separated into train and test folders. 80% of the images of each category were used for training the model and the rest 20% of the images were used to test the model. 
In order to have a better recognition of the food images, we had to optimize our model by reducing the lost function and increasing the accuracy of the model trained. For that reason, two models were trained, one as a classifier of plates only and the other as a classifier of deserts only.
In total, were trained 45 categories of plates and 10 categories of desert.

<p align="center">
  <img width="380" height="250" src="https://scontent.flis5-1.fna.fbcdn.net/v/t1.15752-9/93954898_532133647492527_1163031127477190656_n.png?_nc_cat=107&_nc_sid=b96e70&_nc_ohc=cfFU7gDEoPoAX9fZ_hj&_nc_ht=scontent.flis5-1.fna&oh=e3678ee02559cbac9223d08a10385e45&oe=5EC3C5CE">
</p>


3. **User Options**: On **Yummest App** the user will provide us the image inputs from Plate and Desert and the text inputs from Starter and Drink. The code behind it will calculate the price of those combination of plates and provide to the user the restaurant where that combination is the cheapest.

<p align="center">
  <img width="1000" height="250" src="https://scontent.flis5-1.fna.fbcdn.net/v/t1.15752-9/94357403_230713254663645_3599947050982047744_n.png?_nc_cat=105&_nc_sid=b96e70&_nc_ohc=waAJt4ekO6IAX_74D3c&_nc_ht=scontent.flis5-1.fna&oh=a09425d1adae3f1d98c72307635aee41&oe=5EC5741F">
</p>


4. **Cheapest Restaurant's Location**: Using ***Google Maps*** page and knowing the cheapest restaurant latitud and longitud it's possible to provide the direction for the restaurant.

5. **Tourist Attractions Suggestion**: Using ***Foursquare API*** and by knowing the cheapest restaurant, the app will suggest a maximum of two tourist attractions that the user can visit nearby that restaurant. For this purpose, the functions built will calculate in a 1000 radius a limit of 100 tourist attractions that exist around the restaurant.

<p align="center">
  <img width="650" height="250" src="https://scontent.flis5-1.fna.fbcdn.net/v/t1.15752-9/94566892_222300375742441_7238212906825809920_n.png?_nc_cat=101&_nc_sid=b96e70&_nc_ohc=LgVtHZazUFMAX_6wWeo&_nc_ht=scontent.flis5-1.fna&oh=3ecd083cb4842994db9bb7a92187fcc9&oe=5EC33348">
</p>

6. **Application Display**: Yummest is displayed in a **Tkinter** app (which you can access by typing in your terminal *python package1/tkinter_interface.py*) and in a **Web Page** (which you can access by typing in your terminal *python package1/apy_guay.py* and open the url given in your browser)


## Future improvements
- Add the total calories of each meal.
- Train more categories of plates and deserts, in this case I'll need a more powerful equipment.
- Take the concept of this project into more cities and countries.
