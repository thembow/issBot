# issBot
*a discord bot that works with the International Space Station, art by ig@tomnooker*
![cover art](https://i.imgur.com/gthGBwB.jpg)
![Natural Earth Data](https://www.naturalearthdata.com/wp-content/uploads/2009/08/NEV-Logo-color.png)
![NASA](https://www.earthdata.nasa.gov/s3fs-public/earthdata-oaos-logo-hover.png)
## commands
1. /iss (zoom)- returns where the ISS is currently flying over and gets a satellite image
2. /astronauts - returns a list with wikipedia links of all astronauts currently aboard the ISS
## installation
1. download python 3.10 
2. install required files by running "pip install -r requirements.txt"
   - if you get an issue with py-cord download it directly by running 'pip install git+https://github.com/Pycord-Development/pycord'
3. enter your discord bot token and email into the .env file
4. download ocean from this link and place into this folder
   - https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_geography_marine_polys.zip
5. run the bot.py file
## resources used
1. https://nominatim.org/release-docs/develop/ <- for reverse long/lat lookup
2. http://open-notify.org/ <- for long/lat of ISS and astronauts
3. https://www.mediawiki.org/wiki/API:Main_page <- wikipedia api 
4. https://www.naturalearthdata.com/about/terms-of-use/ <- ocean shape data
5. https://nasa-gibs.github.io/gibs-api-docs/ <- NASA GIBS api
