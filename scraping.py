# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def scrape_all():
    # Initiate headless driver for deployment\
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
                
    except BaseException:
        return None
                
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
                
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def mars_weather(browser):
    # Visit the weather website
    url = 'https://mars.nasa.gov/insight/weather/'
    browser.visit(url)
    
    # Parse the data
    html = browser.html
    weather_soup = soup(html, 'html.parser')
    
    # Scrape the Daily Weather Report table
    weather_table = weather_soup.find('table', class_='mb_table')
    return(weather_table.prettify())
    

def Hemispheres(browser): 
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemisphere = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    Cerberus_img = "https://astrogeology.usgs.gov/cache/images/39d3266553462198bd2fbc4d18fbed17_cerberus_enhanced.tif_thumb.png"
    Cerberus_Title = "Cerebus Hemisphere Enhanced"

    Schiaparalli_img = "https://astrogeology.usgs.gov/cache/images/08eac6e22c07fb1fe72223a79252de20_schiaparelli_enhanced.tif_thumb.png"
    Schiaparalli_Title = "Schiaparelli Hemishphere Enhanced"

    Syrtis_img = "https://astrogeology.usgs.gov/cache/images/55a0a1e2796313fdeafb17c35925e8ac_syrtis_major_enhanced.tif_thumb.png"
    Syrtis_Title = "Syrtis Major Hemisphere Enhanced"

    Valles_img = "https://astrogeology.usgs.gov/cache/images/4e59980c1c57f89c680c0e1ccabbeff1_valles_marineris_enhanced.tif_thumb.png"
    Valles_Title = "Valles Marineris Hemishphere Enhanced"
    
    hemisphere = [{Cerberus_img, Cerberus_Title}, {Schiaparalli_img, Schiaparalli_Title}, {Syrtis_img, Syrtis_Title}, {Valles_img, Valles_Title}]

    # 4. Print the list that holds the dictionary of each image url and title.
    # hemisphere_image_urls

    return (hemisphere)
    
    # 5. Quit the browser
    #browser.quit()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

