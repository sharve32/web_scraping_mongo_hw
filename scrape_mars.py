import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time

def scrape():
    #Dictionary to store all data
    mars_data_dict = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    time.sleep(2)

    #latest news title and paragraph
    news_title = soup.find('div', class_='content_title').text.strip()
    news_para = soup.find('div', class_='rollover_description_inner').text.strip()
    mars_data_dict['news_title'] = news_title
    mars_data_dict['news_para'] = news_para

    #featured image
    featured_img_url = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19334_ip.jpg'
    mars_data_dict['feat_img_url'] = featured_img_url

    #mars weather, from Twitter
    url_twt = 'https://twitter.com/marswxreport?lang=en'
    responded = requests.get(url_twt)
    soups = bs(responded.text, 'lxml')

    #scrape Mars weather tweet
    weather_twt = soups.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[3].text
    mars_data_dict['weather_tweet'] = weather_twt

    #Mars facts
    table = pd.read_html('https://space-facts.com/mars/')[0]
    facts_table = table.rename(columns={table.columns[0]: "Facts"}).rename(columns={table.columns[1]: "Results"})
    mars_data_dict['facts_table'] = facts_table

    #Mars hemispheres
    murl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response_hemi = requests.get(murl)
    soup_hemi = bs(response_hemi.text, 'lxml')
    time.sleep(2)
    titles = soup_hemi.find_all('h3')

    titles_list = []

    #Extract only text value from titles
    for title in titles:
        titles_list.append(title.text)

    #Hardcoded image links
    img_url = ['https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
               'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
               'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
               'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg']
    
    #Create dictionary saving key-value pairs of titles and images
    dict_mars = []
    for x in range(0,4):
        dict_mars.append({'title': titles_list[x], 'imgurl': img_url[x]})
    
    mars_data_dict['dict_mars'] = dict_mars

    return mars_data_dict
