from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs

import config

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)


def findARestaurant(mealType, location):
    # 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    coords = getGeocodeLocation(location)

    # 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    # HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

    url = f'https://api.foursquare.com/v2/venues/search?client_id={config.CLIENT_ID}&client_secret={config.CLIENT_SECRET}&v=20130815&ll={str(coords[0])},{str(coords[1])}&query={mealType}'
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if not result['response']['venues']:
        print(f'No Restaurant found for {location}')
        return 'Restaurant No Found'

    resto = result['response']['venues'][0]['name']
    restaurant_info = {'name': resto}

    # Get Address
    if 'formattedAddress' in result['response']['venues'][0]:
        addr = ', '.join(result['response']['venues'][0]['formattedAddress'])
    else:
        addr = 'Address not Found'

    restaurant_info['address'] = addr

    # Get photo from different api
    resto_id = result['response']['venues'][0]['id']
    url = f'https://api.foursquare.com/v2/venues/{resto_id}/photos'
    photo_response = h.request(url, 'GET')[1]
    result = json.loads(photo_response)

    if result['response']['photos']:
        prefix = result['response']['photos']['items'][0]['prefix']
        suffix = result['response']['photos']['items'][0]['suffix']
        photo_url = prefix + '300x300' + suffix
        print('Restaurant Photo: ' + photo_url)
    else:  # Default
        photo_url = 'https://unsplash.com/photos/RjfZS4XDxQ4'

    restaurant_info['photo'] = photo_url

    print('Restaurant name: ' + resto)
    print('Restaurant photo: ' + photo_url)
    print('Restaurant address: ' + addr)
    return restaurant_info


# 3. Grab the first restaurant
# 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
# 5. Grab the first image
# 6. If no image is available, insert default a image url
# 7. Return a dictionary containing the restaurant name, address, and image url
if __name__ == '__main__':
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney, Australia")
