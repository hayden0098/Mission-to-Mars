# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
# imported dependencies for datetime
import datetime as dt


# In[2]:
# Path to chromedriver
#!which chromedriver


# In[3]:
#==============================================================================
def scrape_all():

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_img(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_data(browser)
        }

    #stop webdriver and return data
    browser.quit()

    return data
#==============================================================================


# ### Visit the NASA Mars News Site
# In[4]:
#=======================================================================================
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        news_p

    except AttributeError:
        return None, None
    
    return news_title, news_p 
#========================================================================================


# ### JPL Space Images Featured Image
# In[9]:
#========================================================================================
def featured_img(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

        # Use the base url to create an absolute url
        img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    except AttributeError:
        return None

    return img_url
#==============================================================================

# ### Mars Facts
# In[14]:
#==============================================================================
def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)

    except BaseException:
        return None

    return df.to_html(classes='table table-striped')
#==============================================================================


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres
# In[17]:
#==============================================================================
def hemisphere_data(browser):

    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    #Parse the resulting html with soup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    try:
        # find all the hemi_mars search result
        hemi_products = hemi_soup.find_all('div', class_='description')

        for i in range(len(hemi_products)):
            # create dictionary
            hemispheres = {}

            # look for the hemisphere image title
            hemi_title = hemi_products[i].find('a').text
            # look for the href link url for that title of image
            href_link = hemi_products[i].find('a',class_ ="itemLink product-item").get('href')
            next_page_url = 'https://astrogeology.usgs.gov'+ href_link

            #visit to next-page via href link url
            browser.visit(next_page_url)
            #Parse the next-page resulting html with soup
            html = browser.html
            img_soup = soup(html, 'html.parser')

            # navigate and get the full-image url
            full_img_url = img_soup.find('li').find('a').get('href')

            # append the titel and img url to list of dictionary
            hemispheres = {'img_url':full_img_url, 'title':hemi_title}
            hemisphere_image_urls.append(hemispheres)

            # browser visit back to the beginning search page
            browser.visit(url)

    except AttributeError:
        return None

    return hemisphere_image_urls
#==============================================================================


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())