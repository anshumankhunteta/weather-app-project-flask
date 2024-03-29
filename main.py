from flask import Flask,render_template,request,abort
import geonamescache
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request
from apikey import apikey

app = Flask(__name__)
def tocelcius(temp):
    return str(round(float(temp) - 273.16,2))
def toFarenhiet(temp):
    return str(round(9 / 5 * (float(temp) - 273.15) + 32, 2))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/',methods=['POST','GET'])
def weather():
    gc = geonamescache.GeonamesCache()
    api_key = apikey
    
    if request.method == 'POST':
        city = request.form['city']
        x=gc.search_cities(city, case_sensitive=False, contains_search=True)
        if len(x)!=0: y=list(x[0].values())
        else: y=["",""]
        city = y[1]
    else:
        #for default name kolkata
        city = 'kolkata'
    
    city = (city.lower()).strip() #remove spaces to avoid errors

    placeholder_data = {"country_code": '404 Not Found',}
    
    # json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return render_template('index.html',data=placeholder_data)
    # converting json data to dictionary

    list_of_data = json.loads(source)

    degree_sign = u"\N{DEGREE SIGN}" # degree symbol

    # data for variable list_of_data
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "temp_cel": tocelcius(list_of_data['main']['temp']) + degree_sign + 'C',
        "temp_far": toFarenhiet(list_of_data['main']['temp']) + degree_sign + 'F',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
        "cityname":str(city).capitalize(),
    }
    return render_template('index.html',data=data)



if __name__ == '__main__':
    app.run(debug=True)