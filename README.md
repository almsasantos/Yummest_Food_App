<img src='https://scontent.flis5-1.fna.fbcdn.net/v/t1.15752-9/92339357_220548049017845_6393812114410045440_n.jpg?_nc_cat=109&_nc_sid=b96e70&_nc_ohc=Wtzo8ySz9AkAX88xMgv&_nc_ht=scontent.flis5-1.fna&oh=9a6af59c3b491b9e9c2310f4d38aff61&oe=5EADB47C' width="180" height="180">

# Yummest

#### Ana Santos - Data Analytics Bootcamp - Ironhack Madrid

# Goal
The goal of Yummest is to help you find the restaurant where your entire meal chosen is the cheapest by passing photos of your plate and desert to the app. 

# Overview
Imagine while traveling to a foreign country you want to eat out to a restaurant but you don't want to spend a lot of money and don't know how to speak its language. The tool needed in those cases will be an app that will allow you to search the specific food you wanna eat based on photos.

This application receives individual pictures of each plate and desert. Based on that information provides you the direction to the restaurant where that full meal is cheaper and gives you suggestions of other tourist attractions nearby that you can visit as well.

# Data
* [El tenedor](https://www.eltenedor.es/)

Data from El Tenedor website was used to make estimations of the cheapest meal, using each menu available in each restaurant page.

* [Food-101 dataset](https://www.kaggle.com/dansbecker/food-101)

Food-101 dataset was used to get the images ready to train the neural network to predict each plate and desert. Each food category was separated into train and test folders. 80% of the images of each category were used for training the model and the rest 20% of the images were used to test the model.

* [Foursquare](https://foursquare.com)

From foursquare API we got the information about tourist attractions nearby the cheapest restaurant.

# Methodology

Once we have each plate's price and the classification models trained, the next step was to create the graphic interface with Tkinter.


# Future improvements
- Add the total calories of each meal.
- Train more categories of plates and deserts, in this case I'll need a more powerful equipment.
- Take the concept of this project into more cities and countries.
