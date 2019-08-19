import os
import requests
from bs4 import BeautifulSoup
from time import sleep


# try and except function
def try_except(page):
    try:
        page.raise_for_status()
    except Exception as exc:
        print("we have a problem!: %s" % (exc))


# set directory where files will be stored
# os.chdir('C:\Program Files\Git\homework-7-jtopper9')

# request homepage of site
homepage = requests.get('https://www.gocomics.com/pearlsbeforeswine/')
try_except(homepage)

# pass the page into the BeautifulSoup module. Return object into soup variable
soup = BeautifulSoup(homepage.text, features="html.parser")

# navigate to latest comics issue through comics tab
comics = soup.select('a[data-link="comics"]')[0]
latest_url = 'https://www.gocomics.com' + comics.get('href')
comics_page = requests.get(latest_url)
try_except(comics_page)


# download latest 10 images from comic issues
images_count = 0
while images_count < 10:
    # pass in comics page into BeautifulSoup
    soup = BeautifulSoup(comics_page.text, features="html.parser")

    # detect image url element
    image = soup.select('picture > img')[1]
    image_url = image.get('src')
    image_res = requests.get(image_url)

    # download image to local directory
    image_file = open(os.path.basename(image_url), 'wb')
    for chunk in image_res.iter_content(100000):
        image_file.write(chunk)
    image_file.close()

    # locate element to access previous comic issue
    previous_button = soup.select\
        ('a[class="fa btn btn-outline-secondary btn-circle fa-caret-left sm js-previous-comic"]')
    previous_url = 'https://www.gocomics.com' + previous_button[0].attrs['href']

    # navigate to previous comic issue
    comics_page = requests.get(previous_url)
    try_except(comics_page)

    images_count += 1
    print("successful image download count = " + str(images_count))
    sleep(1)
