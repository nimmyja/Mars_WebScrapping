from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    dict_val ={'news_title':[],'news_p':[],'featured_image_url':[],'html_table':[],'hemisphere_image_urls':[]}

    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    titles = soup.find_all('div', class_='content_title')
    details = soup.find_all('div', class_='article_teaser_body')
   
    for title in titles:
        dict_val['news_title'].append(title.text)
    for detail in details:
        dict_val['news_p'].append(detail.text)

    browser.quit()

    browser = init_browser()
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    featured_image = soup.find('img', class_='headerimage fade-in')
    featured_image_url = url+featured_image['src']
    dict_val['featured_image_url'].append(featured_image_url)
    browser.quit()


    browser = init_browser()
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    html = browser.html
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = df.columns.get_level_values(0)
    df1 = df.rename(columns = df.iloc[0])
    df2 = df1.rename(columns={'Mars - Earth Comparison': 'Description'})
    df2.set_index(keys='Description',inplace = True)
    
    html_table = df2.to_html()
    dict_val['html_table'].append(html_table)
    browser.quit()

    browser = init_browser()
    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client.mars_db
    collection = db.hemispere
    results = soup.find_all('div', class_='item')

    for x in results:
        title = x.find('h3').text
        print(title)
        image = x.find('img', class_='thumb')
        image_url = url+image['src']
        print(image_url)
    
        # Dictionary to be inserted into MongoDB
        hemisphere_image_urls = {
            'title': title,
            'image_url': image_url
        }
        dict_val['hemisphere_image_urls'].append(hemisphere_image_urls)
        collection.insert_one(hemisphere_image_urls)
        
    browser.quit()  
    



    return dict_val








    
