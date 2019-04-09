
import httplib2
import json
from flask import Flask
from flask import render_template
from flask import request
import sys
import codecs

app = Flask(__name__)

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)



foursquare_client_id = "WLUSFAMZFUBV2LLYFC5FKQUIGBOUUKYIPBWYG5DIFUJ3HVWF"
foursquare_client_secret = "UEAPJJIXEWFQEJGO4DREO4H1QWIILFTVJU4PCFIBPPFMZBW2"


@app.route('/search', methods=['GET', 'POST'])
def findARestaurant():

    if request.method == 'POST':

        place = request.form['place']
        location = place.replace(" ", "+")
        print(location)
        # 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyDQzBHFrZTSHduwMpg5wqL_o0YSZ3hvkdg" % location
        h = httplib2.Http()
        g = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
        lat = g['results'][0]['geometry']['location']['lat']
        lng = g['results'][0]['geometry']['location']['lng']

        # except:
        #     print("Geocode failed")

        meal = request.form['mealType']
        mealType = meal.replace(" ", "+")
        url1 = "https://api.foursquare.com/v2/venues/explore?client_id=%s&client_secret=%s&ll=%s,%s&v=20180323&query=%s" % (
        foursquare_client_id, foursquare_client_secret, lat, lng, mealType)
        h1 = httplib2.Http()
        g1 = json.loads(h1.request(url1, 'GET')[1].decode('utf-8'))
        k = g1['response']['groups'][0]['items']
        

        venues = []
        
        # street = []
        # distance = []

        for i in k:
            
            restaurants = {'name':'No data', 'distance':'No data','address':[]}
            restaurants['name'] = i['venue']['name']
            if i['venue']['location'].get('distance') != None:
                restaurants['distance'] = i['venue']['location']['distance']
            if len(i['venue']['location']['formattedAddress']) != 0:
                for k in i['venue']['location']['formattedAddress']:
                    restaurants['address'].append(k)
            venues.append(restaurants)

            

                
        
        return render_template('restaurantSearch.html', venues = venues)


        # 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
        # HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
        # 3. Grab the first restaurant
        # 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        # 5. Grab the first image
        # 6. If no image is available, insert default a image url
        # 7. Return a dictionary containing the restaurant name, address, and image url
        
    return render_template('restaurantSearch.html', restaurants = None)
    
if __name__ == '__main__':
    app.secret_key = 'super_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000 )
