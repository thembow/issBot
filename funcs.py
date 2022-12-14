import requests
from requests.exceptions import HTTPError
import shapefile
from shapely.geometry import shape, Point
from dotenv import load_dotenv
import os
import sys

load_dotenv()
email = os.getenv('EMAIL')
if not email:
    print('ERROR: Email is missing in .env')
    sys.exit(-1)
#enviroment variable handling
if (os.path.exists("ne_10m_geography_marine_polys.zip")):
    print("Ocean shapefile succesfully found!")
else:
    print("Error! Ocean shapefile not found! Please download ocean from here and place into folder! https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_geography_marine_polys.zip")
    sys.exit(-1)

def astroLookup():
    astronauts = []
    try:
        notifyAstroResponse = requests.get('http://api.open-notify.org/astros.json')
        notifyAstroResponse.raise_for_status()
        notifyAstroJson = notifyAstroResponse.json()
    except HTTPError as http_err:
        print(f'HTTP error!{http_err}')
    except Exception as err:
        print(f'Other error!{err}')
    #catch initial request errors 
    print(f"Response Status: {notifyAstroJson.get('message')}")
    if notifyAstroJson .get('message') != 'success':
        print(f'Error! json request failed at message step!')
    else:
        #loop to get astronauts on the ISS
        for x in notifyAstroJson.get("people"):
                #only loop through the people, we don't care about success value at this point
                    if (x.get("craft")) == "ISS":
                        #gets all astronauts on the ISS
                        astronauts.append(x.get("name"))
    #wikipedia requests
    wUrl = 'https://en.wikipedia.org/w/api.php'
    astrolinks = []
    for x in astronauts:
        query = x
        query = f"intitle: \"{query}\""
        #sets up query correctly to search only for articles with name in title
        params = {
                    "action": "query",
                    "format": "json",
                    "prop": "",
                    "list": "search",
                    "meta": "",
                    "titles": "",
                    "formatversion": "1",
                    "srsearch": query,
                    "srnamespace": "0",
                    "srlimit": "1",
                    "sroffset": "0",
                    "srwhat": "text",
                    "srsort": "relevance"
            #honestly i dont really understand what a lot of these do, but in order to get it to return the correct article these are the correct parameters
            }
        try:
            wikiResponse = requests.get(wUrl, params=params)
            wikiResponse.raise_for_status()
            wikiResponseJson = wikiResponse.json()
        except HTTPError as http_err:
                print(f'HTTP error!{http_err}')
        except Exception as err:
                print(f'Other error!{err}')
            #catch initial request errors 
        title = wikiResponseJson['query']['search'][0]['title']
        link = title.replace(' ', '_')
        link = link.replace('(', '%28')
        link = link.replace(')', '%29')
        #have to replace parentheses or else the link doesnt work
        link = "https://en.wikipedia.org/wiki/"+link
        astrolinks.append(f"[{title}]({link})")
        #creates links
    return astrolinks
    """
    Queries ISS for astronauts currently onboard, returns list of names hyperlinked with their wikipedia

    :return: hyperlinked list of astronauts on iss
    :rtype: list
    :raises HTTPError if request fails
    :raises Error if request fails
    """

def oceanLookup(la, lo): 
    try:
        sf = shapefile.Reader("ne_10m_geography_marine_polys.zip")
    except:
        print("Error! Cannot find ocean shapefile!")
        return "null"
    #file contains data we need to determine coordinate location
    shapes = sf.shapes()
    for x in range(len(shapes)):
        #checks all of the oceans
        cShape = sf.record(x)
        polygon = shape(shapes[x])
        #converts shape to polygon for checking 
        point = Point(float(lo), float(la))
        if polygon.contains(point):
            #if the ocean-polygon contains the point, then the coordinate is located in that ocean.
            print(f"Coordinates found in {cShape[14]}!")
            return cShape[14]
    return "null"
    """
    Checks coordinates using ocean data to determine which ocean a set of coords is in

    :param str la: latitude
    :param str lo: longitude
    :return: name of ocean where found OR null
    :raises Error: if shapefile cannot be found
    """

def issLookup():
    try:
        notifyISS = requests.get("http://api.open-notify.org/iss-now.json")
        notifyISS.raise_for_status()
        notifyISSJson = notifyISS.json()
    except HTTPError as http_err:
        print(f'HTTP error!{http_err}')
    except Exception as err:
        print(f'Other error!{err}')
    long = notifyISSJson['iss_position']['longitude']
    lat = notifyISSJson['iss_position']['latitude']
    #set up long and lat
    print(f"lat: {lat}, long: {long}")
    nomLink = "https://nominatim.openstreetmap.org/reverse?format=json&lat="+lat+"&lon="+long+"&zoom=10&accept-language=en&email="+email
    headers = {
        'User-Agent': 'issBot',
        'From': email  
    }
    #headers
    try:
        nomRequest = requests.get(nomLink, headers=headers)
        nomRequest.raise_for_status()
        nomJson = nomRequest.json()
    except HTTPError as http_err:
        print(f'HTTP error!{http_err}')
    except Exception as err:
        print(f'Other error!{err}')
    if (nomJson.get("error") == "Unable to geocode"):
        print("Unable to geocode, attempting oceanLookup")
        ocean = oceanLookup(lat, long)
        if (ocean == "null"):
            return (lat, long, "null")
        return (lat, long, "the "+ ocean)
    else:
        return (lat, long, nomJson["display_name"])
    """

    issLookup gets the coords of the ISS and tries to reverse lookup. if it fails, it uses oceanLookup
    :return: latitude, longitude, and possible location
    :rtype: tuple 
    :raises HTTPError: if request fails
    :raises Error: if request fails
    """

from datetime import datetime

def parse_date(date_string):
    try:
        #parses date data from string in year-month-day format
        date = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        # If the date string is invalid, return None
        return None

    # If the date string is valid, return the datetime object
    return (str('%02d' % date.year), str('%02d' % date.month), str('%02d' % date.day))
    #tuple to unpack, we have to do string formatting to get it to work with the url, 2012-7-9 doesnt work but 2012-07-09 does
    """

    parse_date takes string input and returns datetime object. if it fails, returns None.
    :return: tuple with year, month, day
    :rtype: tuple
    :param string date_string: string with date info
    :raises ValueError: if date string is invalid 
    """
def coordImg(lat, lon, level, date="2012-07-09"):
    date_valid = True
    lat = float(lat)
    lon = float(lon)
    row = str(int(((90 - lat) * (2 ** level)) // 288))
    col = str(int(((180 + lon) * (2 ** level)) // 288))
    #thank u @lucianpls https://github.com/nasa-gibs/onearth/issues/53#issuecomment-299738858
    #this math gets us an approximate satellite image of the coordinates. its slightly off, fix if u can
    #converts back to int->string for url purposes, same with level below
    level = str(level)
    date_stripped = parse_date(date)
    #strip date information
    if date_stripped is None:
        #to handle errors
        year = "2012"
        month = "07"
        day = "09"
        date_valid = False
    else:
        year, month, day = date_stripped
        #tuple unpacking
    url = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/"+year+"-"+month+"-"+day+"/250m/"+level+"/"+row+"/"+col+".jpg"
    #doesnt work as an f string for some reason so we using +var+
    return (url, date_valid)
    """
    uses NASA GIBS to get a satellite image of where the coordinates are
    :param str lat: latitude
    :param str lon: longitude
    :param int level: level of zoom
    :param string date: date of when image should be taken
    :return: tuple with url, and if date was valid
    :rtype: tuple
    """

