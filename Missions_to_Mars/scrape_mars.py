#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies sopied in from other notebook and repo
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests

# In[2]:

# Set the directory where chromedriver exists
def init_browser():
    executable_path = {'executable_path':'C:/bin/chromedriver.exe'} 
    return Browser('chrome', **executable_path, headless=False)

# In[3]:
def scrape():
    browser = init_browser()
    
    # Visit Nasa news url 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

# In[4]:

    # In[5]:
    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    a_slide = soup.select_one('ul.item_list li.slide') 
    news_title = a_slide.find('div', class_='content_title').find('a').text

    news_snip = a_slide.find('div', class_='article_teaser_body').text
    # Display scraped data 
    print(a_slide)
    print(news_title)
    print(news_snip)

# In[6]:

    # JPL Mars Space Images - Featured Image
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Venus"
    browser.visit(featured_image_url)

    # In[7]:

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_image, "html.parser")

    # Retrieve background-image url from style tag 
    image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = "https://www.jpl.nasa.gov"

    # Concatenate website url with scraped route
    image_url = main_url + image_url

    # Display full link to featured image
    image_url

# In[8]:

    # Mars Weather
    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    time.sleep(1)

    # In[9]:

    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called mars_weather
    
    for tweet in latest_tweets: 
        mars_weather = tweet.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else: 
            pass

    # In[12]:

    # Mars facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    # Use Pandas to "read_html" to parse the URL
    tables = pd.read_html(url)

    # Find Mars Facts DataFrame in the lists of DataFrames
    df = tables[1]

    # Assign the columns
    df.columns = ['Description','Value1', 'Value2']
    html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)
    data = df.to_dict(orient='records') 
    df

    # In[13]:

    # Save html to folder and show as html table string
    mars_facts = df.to_html(classes = 'table table-striped')
    print(mars_facts)

# In[14]:

    # Mars Hemispheres
    # Visit hemispheres website through splinter module 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    # In[15]:

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')
    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored -- for some reason this gave me trouble but 
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs(partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
    # Display hemisphere_image_urls
    hemisphere_image_urls

    #Store all data from scrape function in a dictionary
    mars_dict = {
        "Top_News": news_title,
        "Teaser": news_p,
        "Featured_Image": image_url,
        "Mars_Weather": mars_weather,
        "Mars_Info_Table": html_table,
        "Hemisphere_Title": title,
        "Hemisphere_Image": img_url
        }
    
    # close the browser
    browser.quit()

    # return the results
    return mars_dict