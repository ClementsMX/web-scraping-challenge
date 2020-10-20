#dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

import requests
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()

    # Empty dictionary to hold all findings
    findings_dict = {}
    
    # NASA MARS NEWS
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(3)

    nasa_html = browser.html
    soup = BeautifulSoup(nasa_html, "html.parser")

    first_news = soup.find_all("div", class_="list_text")[0]
    
    news_title = first_news.find(class_="content_title").text
    #news_title
    news_p = first_news.find(class_="article_teaser_body").text
    #news_p
    

    # JPL Mars Space Images - Featured Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2) 

    time.sleep(2)

    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")

    #base url for the images
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/"

    image_section = soup.find('article', class_="carousel_item")['style']
    #image_section

    image_name= (image_section.split("wallpaper/")[1]).split("')")[0]
    #image_name
    featured_image_url= jpl_url + image_name

    # Mars Weather
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)

    time.sleep(3)

    twitter_html= browser.html
    soup= BeautifulSoup(twitter_html, "html.parser")

    mars_weather = (soup.find('div', attrs={"data-testid": "tweet"}).get_text()).split('InSight ')[1]
    #mars_weather

    #MARS FACTS
    url4 = "https://space-facts.com/mars/"

    mars_table = pd.read_html(url4)
    data_table = pd.DataFrame(mars_table[0])

    #data_table

    data_table = data_table.rename(columns={0 : "Description",
                                        1 : "Value"})
    data_table.set_index("Description", inplace = True)

    table_html = data_table.to_html()
    table_html= table_html.replace('\n',"")
    #table_html

    # Mars Hemisphere
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"
    browser.visit(url5)

    time.sleep(3)


    hemisphere_html = browser.html
    soup = BeautifulSoup(hemisphere_html, 'html.parser')

    #To save urls
    hemisphere_urls = []

    hemispheres = soup.find_all("div", class_ = "description")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text.strip("Enhanced")
        browser.click_link_by_partial_text(title)
        next_html = browser.html

        soup_next = BeautifulSoup(next_html, 'html.parser')

        image_url = soup_next.find("img", class_ = "wide-image")["src"]
        img_url = base_url + image_url
        
        info_dict = {"title" : title,"img_url" : img_url}
        hemisphere_urls.append(info_dict)

    # Filling the dictionary
    findings_dict["news_title"] = news_title
    findings_dict["news_p"] = news_p
    findings_dict["featured_image_url"] = featured_image_url
    findings_dict["mars_weather"] = mars_weather
    findings_dict["mars_facts"] = table_html
    findings_dict["hemisphere_image_urls"] = hemisphere_urls
    
    # After scraping
    browser.quit()

    # Return results
    return findings_dict

