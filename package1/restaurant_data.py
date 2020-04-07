import pandas as pd
from urllib.request import urlopen
import regex as re
import json
from pandas.io.json import json_normalize
import glob


list_of_websites = glob.glob('/data/webs/*.html')
#see how many restaurant do we have:
len(list_of_websites)


def restaurant_data():
    for web in list_of_websites[:5]:
        try:
            url = pd.read_html(web)
            url = url[0][1][30]
            restaurant = str(re.search(r'<script id="restaurant_jsonld"(.*)}</script><div class="', url))
            b = re.sub("<regex.Match object; span=(.*), match=\'<script id=", '', restaurant)
            c = b.replace('"restaurant_jsonld" type="application/ld+json">', '')
            d = c.replace('</script><div class="', '')
            e = d.replace("'>", '')
            data = json.loads(e)
            json_file = pd.json_normalize(data)
            restaurant_name = str(json_file['name'])

            rest = restaurant_name.replace('\nName: name, dtype: object', '')
            restaurant_cor = rest.replace('0    ', '')
            restaurant_correct = restaurant_cor.replace('Menú del restaurante ', '')
            plates = []
            num = []

            search_rating = str(re.search(
                r'Ratings":{"thefork":{"ratingValue":[+-]?([0-9]*[.])?[0-9]+,"reviewCount":[+-]?([0-9]*[.])?[0-9]+}',
                url))
            almost_rating = re.sub("<regex.Match object; span=(.*), match=\'Ratings", '', search_rating)
            rate_b = almost_rating.replace('":{"thefork":{"ratingValue":', '')
            rate_c = rate_b.replace('"reviewCount":', '')
            rate_d = rate_c.replace("'>", '')
            rate_e = rate_d.replace('}', '')
            rate_f = re.sub(',[+-]?([0-9]*[.])?[0-9]+', '', rate_e)

            search_cuisine = str(re.search(r'"servesCuisine":"\w*"', url))
            almost_cuisine = re.sub("<regex.Match object; span=(.*), match=\'", '', search_cuisine)
            cuisine_b = almost_cuisine.replace('"servesCuisine":', '')
            cuisine = cuisine_b.replace("'>", '')

            search_street = str(re.search(r'"address":{"street":"\w+( +\w+)*', url))
            almost_street = re.sub("<regex.Match object; span=(.*), match=\'", '', search_street)
            street_b = almost_street.replace('address":{"street":"', '')
            street = street_b.replace("'>", '')

            search_geo = str(re.search(r'<script>window.__INITIAL_STATE__ = (.*);</script>', url))
            geo_b = re.sub("<regex.Match object; span=(.*), match='<script>window.__INITIAL_STATE__ = ", '', search_geo)
            geo_c = geo_b.replace("</script><script>window.__APOLLO_STATE__={};</script>'>", '')
            almost_latitude = re.findall(r'"geo":{"latitude":[-+]?\d*\.*\d+,"longitude":[-+]?\d*\.*\d+', geo_c)

            col_plate = []
            for i in range(0, len(data['hasMenuSection'])):
                col_plate.append(str(json_file['hasMenuSection'][0][i]['name']))
                plates.append(json_file['hasMenuSection'].to_dict()[0][i]['hasMenuItem'])
                num.append(str(i) + str(restaurant_name))

            for j in range(0, len(plates)):
                df1 = pd.json_normalize(plates[j])
                df1['type_of_plate'] = col_plate[j]
                df1['rating'] = rate_f
                df1['cuisine'] = cuisine
                df1['direction'] = street
                df1['geo'] = almost_latitude[0]
                df1.to_csv('/data/csv_each_restaurants/' + str(j) + str(restaurant_correct) + '.csv')

            for file in glob.glob('/data/csv_each_restaurants/*.csv'):
                if restaurant_correct in file:
                    df = pd.read_csv(file)
                    df['restaurant'] = restaurant_correct
                    df.to_csv(file)

        except:
            pass

def merge_to_csv():
    dfs = glob.glob('data/csv_each_restaurants/*.csv')

    result = pd.concat([pd.read_csv(df) for df in dfs], ignore_index=True)

    result.to_csv('merge1.csv')
    print('you have the merge file created!')

restaurant_data()
merge_to_csv()
