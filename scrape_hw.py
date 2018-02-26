from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time
from selenium import webdriver
from flask import Markup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}
    news_title = []
    news_p = []
    hemisphere_image_urls = []
    image_dict = {}
    scrape_dict = {}
#    scrape_dict = {[news_title], [news_p], [hemisphere_image_urls], image_dict}

    
    news_url = 'https://mars.nasa.gov/news/'
    response = requests.get(news_url)
    soup = bs(response.text, 'html.parser')
    results_title = soup.find_all('div', class_='content_title')
    results_text = soup.find_all('div', class_='rollover_description_inner')
    for result in results_title:
        title = result.find('a').text.strip()
        link = result.find('a').get('href')
        news_title.append(title)

    for result in results_text:
        text = result.text.strip()
        news_p.append(text)

    scrape_dict['title'] = news_title
    scrape_dict['news'] = news_p

#    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
#    browser = Browser('chrome', **executable_path, headless=False)
    image_url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(image_url)
    for x in range(1):
        html = browser.html
        soup = bs(html, 'html.parser')
        image_link = soup.find('article', class_='carousel_item').get('style')
        image_link = image_link[36:]
        image_link = image_link[:-3]
        feature_image_url = image_url + image_link

    scrape_dict['feature_image'] = feature_image_url


#    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
#    browser = Browser('chrome', **executable_path, headless=False)
    twit_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twit_url)
    for x in range(1):
        html = browser.html
        soup = bs(html, 'html.parser')
        mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    scrape_dict['weather'] = mars_weather


    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    tables[0].columns = ['characteristic', 'value']
    mars_df = tables[0]
    mars_dict = mars_df.to_dict('records')
    scrape_dict['facts'] = mars_dict

#    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
#    browser = Browser('chrome', **executable_path, headless=False)
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    
    for x in range(1):
        html = browser.html
        soup = bs(html, 'html.parser')
        mars_image_group = soup.find_all('div', class_='collapsible results')
    
    
        for item in mars_image_group:
            image_items = item.findAll('div', class_='item')
 

            for link in image_items:
                image_link = link.find('a').get('href')
                image_link = image_link[24:]
                image_text = link.find('h3').text
                image_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/' + image_link + '.tif/full.jpg'
                image_dict = {'title':image_text, 'image_url': image_url}
                hemisphere_image_urls.append(image_dict)
    
    scrape_dict['hemisphere'] = hemisphere_image_urls

#    scrape_dict = {
#    'news_p' : [news_p],
#    'feature_image' : feature_image_url,
#    'mars_weather' : mars_weather,
#    'image' : [hemisphere_image_urls],
#    'facts' : mars_html
#    }

    return scrape_dict

#    url = "https://raleigh.craigslist.org/search/hhh?max_price=1500&availabilityMode=0"
#    browser.visit(url)
#    time.sleep(1)

#    html = browser.html
#    soup = BeautifulSoup(html, "html.parser")

#    listings["headline"] = soup.find("a", class_="result-title").get_text()
#    listings["price"] = soup.find("span", class_="result-price").get_text()
#    listings["hood"] = soup.find("span", class_="result-hood").get_text()
