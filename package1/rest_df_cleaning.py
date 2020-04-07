import pandas as pd
import regex as re


def cleaning_data():
    #read csv file
    df_rest = pd.read_csv('../data/merge1.csv')

    # removing null values
    df_rest = df_rest.loc[:, ~df_rest.columns.str.contains('^Unnamed')]

    # removing columns:
    drop_columns = ['description', '@type', 'offers.@type', 'offers.priceCurrency']
    df_rest = df_rest.drop(drop_columns, axis=1)
    df_rest.dropna(inplace=True)

    #adding latitude and longitude informations:
    lat = []
    log = []
    for i in df_rest['geo']:
        i=f"'{i}'"
        lat_long=re.findall(r'[-+]?\d*\.*\d+', i)
        lat.append(lat_long[0])
        log.append(lat_long[1])
    df_rest['lat'] = lat
    df_rest['log'] = log

    #adding type of cuisine of the restaurante:
    cuisine = []
    for i in df_rest['cuisine']:
        cuisine.append(i.replace('"', ''))
    df_rest['cuisine'] = cuisine

    # rename columns:
    df_rest = df_rest.drop(['direction', 'geo'], axis=1)
    df_rest.columns = ['product', 'price', 'type', 'rating', 'cuisine', 'restaurant', 'lat', 'log']

    # all values in lowercase:
    df_rest = df_rest.apply(lambda x: x.astype(str).str.lower())

    df_rest['price'].replace(',', '.', inplace=True)

    food_type_corrections = {'menú (bebidas excluidas)': 'plato',
                             'tartar, tiraditos, sashimis': 'postre',
                             'platos elaborados': 'plato',
                             'bebidas': 'bebida',
                             'entrantes': 'entrante',
                             'postres': 'postre',
                             'nuestras salsas caseras': 'salsa',
                             'ensaladas': 'ensalada',
                             'vegetarianos': 'plato - vegetariano',
                             'recomendaciones': 'plato',
                             'especialidades queen': 'plato',
                             'arroces y fideua': 'plato - arroz',
                             'gratinati e risotto': 'plato - risotto',
                             'huevos con fundamento, con la yema bien amarillita': 'plato',
                             'salteado de arroz al wok con verduras de temporada': 'plato - arroz',
                             'arroz y tallarines': 'plato - arroz',
                             'ensaladas y sopas': 'ensalada',
                             'tapas y raciones': 'plato', 'carnes y pescados': 'plato',
                             'ensaladas y verduras': 'ensalada',
                             'pescados y mariscos': 'plato',
                             'verduras y tofu': 'plato',
                             'hot-dog y costillas - acompañados con patatas fritas o nachos orlando': 'plato',
                             'guiso y nabe': 'plato',
                             'zumos y batidos': 'bebida',
                             'tortilla de espinaca y patatas confitadas': 'plato',
                             'cordero curry': 'plato', 'arroces y pescados': 'plato',
                             'arroces y fideo': 'plato - arroz',
                             'zumos naturales y smoothies': 'bebida',
                             'entrantes y primeros platos': 'plato',
                             'platos y sancocho': 'plato',
                             'parrillas y braseria': 'plato',
                             'zumos y cocteles de frutas': 'bebidas',
                             'arroces y pastas': 'plato',
                             'risotti / arroces ( min 2 personas)': 'plato - arroz',
                             'platos de biryani': 'plato',
                             'platos principales -pollo a la brasa': 'plato',
                             'curry con vegetales y quinoa roja bio salteada': 'plato',
                             'entremeses y sopas': 'plato',
                             'chacinas finas y quesos gallegos': 'entrante',
                             'pasta tadizionale - elige la variedad de pasta que más te gusta y acompáñala con una de nuestras salsas artesanales': 'plato',
                             'pregunte por nuestros guisos y platos del día': 'plato',
                             'pollo de corral y pato': 'plato',
                             'verduras curry': 'plato',
                             'con los mejores huevos camperos': 'plato',
                             'menu infantil': 'plato',
                             'arroces y pasta': 'plato',
                             'comidas y cenas': 'plato',
                             'sushi bar nigiris y sashimi': 'plato',
                             'mariscos y pescados': 'plato',
                             'menú sushi y sashimi': 'plato',
                             'nuestras ensaladas y guarniciones': 'ensalada',
                             'o crea tu propia hamburguesa - todas las hamburguesas se sirve con base de lechuga, tomate y cebolla morada': 'plato',
                             'verduras y ensaladas': 'ensalada',
                             'calzone y stromboli': 'salsa',
                             'pizzas y calzones': 'pizza',
                             'platos de tandoori (especialidades)': 'plato',
                             'menú del dia': 'plato',
                             'nuestros txuletones': 'plato',
                             'guarnicion': 'plato',
                             'taiyaki': 'postre',
                             'cordero (curries)': 'plato',
                             'postres sin gluten': 'postre',
                             'gambas curry': 'plato',
                             'menú degustación': ' plato',
                             'los guisos': 'plato',
                             'de la huerta a la mesa': 'plato',
                             '¿pedimos una ensalada?': 'ensalada',
                             'gyoza artesanas de rabo de toro con foie': 'plato',
                             'individuales para empezar': 'entrante',
                             'tartare - tartare': 'plato',
                             'pollo (curries)': 'plato',
                             'los pulpos de mila': 'plato',
                             'maki (6 unidades)': 'plato',
                             'paste fresche e secche / pastas frescas y secas': 'plato',
                             'embutidos, compartir y quesos': 'entrante',
                             'de nuestros campos y mares': 'plato',
                             'raciones y platos': 'plato',
                             'recetas vegetarianos y veganos': 'plato',
                             'tostas (con pan cristal) y sandwiches': 'plato',
                             'carnes y aves': 'plato',
                             'empezar y compartir / to start and share': 'entrante',
                             'entrantes, ensaladas y verduras': 'entrante - ensalada',
                             'entradas y picoteo': 'entrante',
                             'carnes y pesacados': 'plato',
                             'sandwich y bagel (all day)': 'plato',
                             'selezione di carne': 'plato',
                             'nuestra parrilla de carbón': 'plato',
                             'productos del mar': 'plato',
                             'tapiocas (tortilla de harina de yuca. sin gluten)': 'plato',
                             'verduras y legumbres': 'plato',
                             'tallarines y arooz': 'plato',
                             'nuestros arroces y fideuás': 'plato',
                             'pasta ripiena - elige la variedad de pasta que más te gusta y acompáñala con una de nuestras salsas artesanales': 'plato',
                             'arroz y noodles': 'plato - arroz',
                             'tartares y sashimis': 'plato',
                             'desayuno y merienda': 'entrante',
                             'sopas y guisos': 'plato',
                             'primeros y segundos': 'plato',
                             'sopas y arroces': 'plato',
                             'hamburguesas y hot dogs': 'plato',
                             'aves y carnes': ' plato',
                             'sugerecias en ensaladas': 'ensalada',
                             'pastas y arroces': 'plato',
                             'aves y caza': 'plato',
                             'entrantes frios y ensaladas': 'entrante - ensalada',
                             'pescado y marisco': 'plato',
                             'sugerencias de tapas y raciones': 'plato',
                             'arroces y noodles': 'plato',
                             'de los valles y montañas de asturias': 'plato',
                             'tou fu': 'plato',
                             'pato lakeado crispy': 'plato',
                             'platos caseros': 'plato',
                             'tortillitas (all day)': 'plato',
                             'nuestros sorbetes': 'plato',
                             'ensaladas verduras y hortalizas': 'ensalada',
                             'ensaladas, pasta y arroces': 'ensalada - plato',
                             'platos tradicionales persa': 'plato',
                             'miss éxitos en rolls tempurizados': 'plato',
                             'plato do de tandoori / horno': 'plato',
                             'sánwiches': 'plato',
                             'nuestros guisos del día...': 'plato',
                             'croquetas…..': 'plato',
                             'de la montaña y las granjas': 'plato',
                             'dulces y goloseo….': 'postre',
                             '…zuria y el mar': 'plato',
                             'perros y wraps': 'plato',
                             'rollitos dumpling y bahn cuon': 'plato',
                             'pollo curry': 'plato',
                             'tartar, tiraditos y sashimi': 'plato',
                             'verdes y frescos': 'plato',
                             'hamburguesas y perritos': 'plato',
                             'cremas, ensaladas y otros platos frios': 'ensalada - plato',
                             'sopa y ramen': 'plato',
                             'bocadillos y sandwiches': 'plato',
                             'platos de gambas y pescado': 'plato',
                             'langostinos curry': 'plato',
                             'guarnición': 'plato',
                             'diseña tu bowl con tus ingredientes favoritos': 'plato',
                             'caldosos (mínimo dos personas, precio por persona)': 'plato',
                             'la empanada y las tortillas': 'plato',
                             'blinis y nalisniki': 'postre',
                             'chhurpi; marinado con queso nata,especias y hierbas.': 'plato',
                             'safari; marinado con yogur, menta, especias y hierbas.': 'plato',
                             'para los peques': 'plato',
                             'huerta': 'plato',
                             'los postres': 'postre',
                             'cazuela caliente': 'plato',
                             'nigiri sushi': 'plato',
                             'entrantes y ensalada': 'ensalada - entrante',
                             'arroz y fideos': 'plato - arroz',
                             'hamburguesas (escoge tu carne y van acompañadas con patatas graal)': 'plato',
                             'la cuchara y el puchero': 'plato',
                             'arroz, pescados y mariscos': 'plato',
                             '…carnes y guisos': 'plato',
                             'dulces divertidos y de colores': 'postre',
                             'beef': 'plato',
                             'menús de temporada 2018': 'plato',
                             'pastas y fideos': 'plato',
                             'platos combinados y parrilla': 'plato',
                             'pepitos ((escoge tu carne y van acompañadas con patatas graal))': 'plato',
                             'ensaladas y cremas': 'ensalada - crema',
                             'ensaladas y entrantes': 'ensalada - entrante',
                             'kathmandu dishes; preparado con nueces, nata, carne picada y huevos con sabor especial.': 'plato',
                             'variantes y ultramarinos': 'plato',
                             'chacinas y salazones': 'entrante',
                             'embutidos y salazones': 'entrante',
                             'chacinas, quesos y salazones': 'entrante',
                             'chacinas, salazones y foie': 'entrante',
                             'enchiladas': 'plato',
                             'ternera (curries)': 'plato',
                             'wraps': 'plato',
                             'embutidos y quesos': 'entrante',
                             'ensaladas y verduras a la parrilla': 'ensalada',
                             'postres y bebidas': 'postre - bebida',
                             'arroces y entrantes': 'entrante',
                             'ensaladas frescas y verduras': 'ensalada',
                             'raciones y sugerencias para compartir ... o no': 'plato',
                             'pasta y arroces': 'plato',
                             'pahadi; marinado con chili, ajo,jengibre, especias, hierbas y asado en el horno tandoori': 'plato',
                             'arroces (mínimo 2 p.) precio por persona elaborados con el mejor arroz de calasparra. arroces secos y caldosos': 'plato - arroz',
                             'platos para acompañar y aperitivos': 'plato',
                             'emtrantes y fritos': 'entrante',
                             'patatas y huevos': 'entrante',
                             'pescados, carnes y más': 'plato',
                             'cremas y sopas': 'plato',
                             'pescados y carnes': 'plato',
                             'carne y pescado': 'plato',
                             'tostas y entrepanes': 'plato',
                             'sopas y caldos': 'plato',
                             'carnes y guisos…..': 'plato',
                             'zuría y el mar…..': 'plato',
                             'pasta y arroz': 'plato',
                             'fondues y carnes': 'plato',
                             'mariscos y pescados salvajes': 'plato',
                             'verduras y hortalizas': 'plato',
                             'pizzas y hamburguesas': 'plato',
                             'pahadi; marinado con chili, ajo,jengibre, especias, hierbas y asado en el horno tandoori.': 'plato',
                             'arroces y paellas': 'plato',
                             'noodles y arroces': 'plato - arroz',
                             'arroz y pasta': 'plato',
                             'tallarines y arroces': 'plato - arroz',
                             'verdes, frescas y curiosas': 'plato',
                             'lumbini sekuwa; cocinando con pimientos, cebolla, tomate, ajo jengibre y hierbas.': 'plato',
                             'tandoori especial (plato asado en plancha caliente, marinado con yogur, jengibre, ajos, limón y especias)': 'plato',
                             'tortas y burritos': 'plato',
                             'ensaladas frescas y verduras....': 'ensalada',
                             'huevería y croquetas': 'plato',
                             'nuestra especialidad: el arroz y la paella': 'plato - arroz',
                             'caviar y ahumados': 'plato',
                             'sugerencias del día y platos de temporada': 'plato',
                             'condimentos y salsas': 'salsa',
                             'himalaya ross dishes; preparado con frutos secos, salsa de tomate, nata y hierbas de himalaya.': 'plato',
                             'everest chilli garlic dishes; preparado con chili,ajo, pimientos,cebolla, tomate, cilantro, especias y hierbas.': 'plato',
                             'achari; marinado al estilo tikka, con salsa incurtdos ácidos y asado en el horno tandoori.': 'plato',
                             'quesos e ibéricos del país (con picos andaluces y pan recién tostado)': 'entrante',
                             'mustang dishes; preparado con salsa de anacardos, hierbas, especias, nata y loquera de manzana.': 'plato',
                             'mango dishes; cocinando con mango, nata almendras,especias y hierbas.': 'plato',
                             'nuestros arroces y fideuá (mín. 2 personas) precio por persona - hacemos los arroces secos y caldosos': 'plato',
                             'verduras, primeros platos y arroces': 'plato',
                             'mint sekuwa; cocinando con yogur, menta fresca, ajo jengibre y hierbas de himalaya.': 'plato',
                             'pokhara garlic; rebozado y cocinado con ajo jengibre,yogur, pimiento,cebolla, especias y hierbas.': 'plato',
                             'kesar dishes; preparado con almendras, tomate, salsa curry, nata, hierbas y especias.': 'plato',
                             'castizo y de cuchara.': 'plato',
                             'kasmiri dishes; preparado con fruta mixta, almendras, yogur, nata, especias y hierbas': 'plato',
                             'kasmiri dishes; preparado con fruta mixta, almendras, yogur, nata, especias y hierbas.': 'plato',
                             'sopas y cremas': 'plato',
                             'chacinas finas, quesos y salazones': 'entrante',
                             'green valley dishes; preparado con hierbas de himalaya, espinacas nueces y menta.': 'plato',
                             'sushis combinados': 'plato',
                             'guiso tradicional japonés': 'plato',
                             'japanese wagyu beef': 'plato',
                             'ceviches y tiraditos': 'plato',
                             'arroz y fideo': 'plato',
                             'fondues y raclettes': 'plato',
                             'tostas (all day)': 'plato',
                             'bandejas': 'entrante',
                             'nuestros bowls': 'plato',
                             'frescas ensaladas': 'ensalada',
                             'mare e monti': 'plato',
                             'dulces': 'postre',
                             'irresistibles postres': 'postre',
                             'dolci artigianali': 'postre',
                             'sushi & sashimi variado': 'plato',
                             'uramaki': 'plato',
                             'platos veggie': 'plato',
                             'nuetras hamburguesas': 'plato',
                             'milanesas': 'plato',
                             'dumplings': 'plato',
                             'nuestros helados': 'postre'}

    for k, v in food_type_corrections.items():
        df_rest.type.replace(k, v, inplace=True)

    for plate in df_rest['type']:
        if 'plato' in plate or 'platos' in plate or 'parrilla' in plate or 'temporada' in plate or 'clásicos' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'ensalada' in plate or 'insalate' in plate:
            df_rest.type.replace(plate, 'ensalada', inplace=True)
        elif 'carne' in plate or 'carnes' in plate or 'steak' in plate or 'mar' in plate or 'calientes' in plate or 'empanada' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'pescado' in plate or 'burgers' in plate or 'burger' in plate or 'cocina' in plate or 'muy crudo' in plate or 'perú' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'arroces' in plate or 'arroz' in plate or 'raciones' in plate or 'cooking' in plate or 'tosta' in plate or 'basmati' in plate or 'burguer' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'crema' in plate or 'sopa' in plate or 'princpales' in plate or 'primeros' in plate or 'receta' in plate or 'comida' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'dulce' in plate or 'dulces' in plate or 'postre' in plate:
            df_rest.type.replace(plate, 'postre', inplace=True)
        elif 'pasta' in plate or 'pizza' in plate or 'tortilla' in plate or 'principales' in plate or 'sashimi' in plate or 'hamburguesa' in plate or 'al vapor' in plate or 'tallarin' in plate or 'maki' in plate or 'dim sum' in plate or 'costilla' in plate or 'ceviche' in plate or 'cuchara' in plate or 'tandoori' in plate or 'cerdo' in plate or 'brasa' in plate or 'ave' in plate or 'wok' in plate or 'chicken' in plate or 'forno' in plate or 'risotti' in plate or 'verde' in plate or 'plancha' in plate or 'horno' in plate or 'ramen' in plate or 'lobster' in plate or 'grill' in plate or 'cook' in plate or 'huerta' in plate or 'secondi piatti' in plate or 'primi piatti' in plate or 'chef' in plate or 'asturia' in plate or 'salmón' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'sushi' in plate or 'sandwiches' in plate or 'sándwiches' in plate or 'hmburguesas' in plate or 'segundos' in plate or 'huevos' in plate or 'tempura' in plate or 'arepas' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'marisco' in plate or 'verduras' in plate or 'verdura' in plate or 'paella' in plate or 'acompañamientos' in plate or 'continua' in plate or 'tierra' in plate or 'carnicería' in plate or 'frito' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'bollería' in plate or 'helado' in plate or 'tarta' in plate or 'crep' in plate or 'dolci' in plate:
            df_rest.type.replace(plate, 'postre', inplace=True)
        elif 'cordero' in plate or 'rolls' in plate or 'wraps' in plate or 'fries' in plate or 'pig' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'de la huerta' in plate or 'pollo' in plate or 'especiales' in plate or 'bocadillos' in plate or 'especialidades' in plate or 'comer' in plate or 'curry' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'para picar' in plate or 'compartir' in plate or 'entrantes' in plate or 'aperitivos' in plate or 'tapas' in plate or 'comenzar' in plate or 'empezamos' in plate or 'empezar' in plate or 'entrada' in plate or 'antipasti' in plate or 'pica' in plate or 'hummus' in plate or 'pikoteo' in plate or 'empezando' in plate or 'antipasto' in plate or 'tapeo' in plate or 'picoteo' in plate or 'aperritivos' in plate or 'barra' in plate or 'tapita' in plate or 'tapeando' in plate or 'para abrir boca' in plate:
            df_rest.type.replace(plate, 'entrante', inplace=True)
        elif 'pescadería' in plate or 'solo para mí' in plate or 'bacalao' in plate or 'guarniciones' in plate or 'ternera' in plate or 'hmburguesas' in plate or 'pato' in plate or 'nigiri' in plate or 'roll' in plate or 'croqueta' in plate or 'sandwich' in plate:
            df_rest.type.replace(plate, 'plato', inplace=True)
        elif 'vino' in plate or 'cerveza' in plate or 'coctelería' in plate or 'café' in plate or 'cafe' in plate or 'infusiones' in plate or 'bebida' in plate or 'cocktail' in plate or 'rioja' in plate or 'smoothies' in plate or 'jugos' in plate or 'cócteles' in plate:
            df_rest.type.replace(plate, 'bebida', inplace=True)

    df_rest['type'].replace('ensalada', 'plato', inplace=True)
    print(df_rest['type'].value_counts())

    good_dict = {'á': 'a', 'à': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    df_rest.replace(good_dict, regex=True, inplace=True)

    df_rest = df_rest[df_rest.groupby('type').type.transform(len) > 570]
    df_rest.to_csv('../data/restaurant_dataframe.csv')

cleaning_data()