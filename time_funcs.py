from PIL import Image
from funcs import *
import os
from datetime import datetime, timedelta
from exceptions import *

def is_image_mostly_black(image_path, threshold=0.5):
    """checks if supplied image file is mostly black

    Args:
        image_path (str): image filename/path
        threshold (float, optional): What percentage black to fail. Defaults to 0.5.

    Returns:
        _type_: _description_
    """
    # Open the image file using the Image module from the Python Imaging Library (PIL)
    image = Image.open(image_path)

    # Convert the image to a grayscale image (which will only have one channel instead of three)
    # This is useful because it allows us to easily check if a pixel is black
    image = image.convert("L")

    # Get the width and height of the image
    width, height = image.size

    # Initialize a counter for the number of black pixels in the image
    num_black_pixels = 0

    # Iterate through all pixels in the image
    for x in range(width):
        for y in range(height):
            # Get the pixel value at (x, y)
            pixel = image.getpixel((x, y))

            # If the pixel is black (i.e. it has a value of 0), increment the counter
            if pixel == 0:
                num_black_pixels += 1

    # Calculate the fraction of black pixels in the image
    black_pixel_fraction = num_black_pixels / (width * height)

    # If the fraction of black pixels is greater than or equal to the threshold, return True
    if black_pixel_fraction >= threshold:
        return True

    # Otherwise, return False
    return False

import requests

def download_image(image_url, save_path):
    """downloads and saves image from url

    Args:
        image_url (string): http url
        save_path (string): filename to save as
    """
    # Send a GET request to the image URL
    response = requests.get(image_url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        print("gibs url query response succesful!")
        # Open a file in write-binary mode at the specified save path
        with open(save_path, "wb") as file:
            # Write the image data to the file
            file.write(response.content)
    else:
        print(f"Failed to download image from URL: {image_url}")

def time_travel(lat, long, date, zoom=5):
    """Tries to get satellite image at specified date

    Args:
        lat (int): latitude
        long (int): longitude
        date (str): when image should be taken, YEAR-MONTH-DAY format.
        zoom (int, optional): _description_. Defaults to 5.

    Raises:
        InvalidDateException: if date supplied is bad
        InvalidDateException: if coordImg raises InvalidDate exception

    Returns:
        url (str): url or None if fail
    """
    date_converted = parse_date(date)
    #converts to datetime object
    if date_converted is None:
        #if it is invalid
        date = "2012-07-09"
        print("date supplied is bad, defaulting to 2012-07-09")
        raise InvalidDateException
    #makes sure date is valid
    counter = 0
    #makes sure we dont try too many times
    while counter <= 4: 
        try:
            cI = coordImg(lat, long, date)
            #attempt to get url
        except InvalidDateException:
            raise InvalidDateException
        download_image(cI, "current.jpg")
        #get image at date
        mostly_black = is_image_mostly_black("current.jpg", threshold=0.5)
        #checks image
        print(f"Image mostly black? {mostly_black}")
        delete_file("current.jpg")
        if mostly_black:
            #if image at url is mostly black
            new_date = date_converted - timedelta(days=1)
            new_date = f"{str('%02d' % new_date.year)}-{str('%02d' % new_date.month)}-{str('%02d' % new_date.day)}"
            print(f"Error! Could not retrieve image from date: {date}, Trying {new_date}")
            counter = counter + 1
        print("Succesfully found image!")
        return cI
    print("Could not successfully find image! :(")
    return None
    #if we cant get a valid image/url

def delete_file(file_name):
    """Deletes file

    Args:
        file_name (str): filename to delete
    """
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"File: {file_name} deleted!")
    else:
        print(f"Error! File: {file_name} not found")

iss = issLookup()
try:    
    time_travel(iss[0], iss[1], "777")
except InvalidDateException:
    print("DATE WAS INVALID!!")
