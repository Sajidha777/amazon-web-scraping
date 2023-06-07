from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#function for extracting title
def get_title(soup):
    
    try:
        title=soup.find("span",attrs={"id":'productTitle'}).text.strip()
        
    except AttributeError:
        title=""
        
    return title


#fuction for extracting price
def get_price(soup):

    try:
        price = soup.find("span",attrs={'class':'a-price-whole'}).text

    except AttributeError:

        price = ""

    return price

#function for extracting rating 
def get_rating(soup):

    try:
        rating = soup.find("span",attrs={'class':'a-icon-alt'}).text
    
    except AttributeError:	
        rating = ""
    return rating
    
#fuctin for extracting count of ratings
def get_review_count(soup):
    try:
        review_count = soup.find("span",attrs={'id':'acrCustomerReviewText'}).text

    except AttributeError:
        review_count = ""	

    return review_count


#function for extracting ingredients
def get_ingredients(soup):
    try:
        ingredients=""
        infos = soup.find("div",attrs={'id':'important-information'}).find_all('div',attrs={'class':'a-section content'})
        txt='Ingredients:'
        for sub_div in infos:
            h4=sub_div.find('h4')
            if h4 and txt in h4.text:
                p=h4.find_next_sibling('p')
                if p:
                    ingredients = p.get_text(strip=True)
    
    except:
        ingredients = ""
    
    return ingredients


#get brand
def get_brand(soup):
    try:
        brand = new_soup.find('div',attrs={'class':'a-section brand-snapshot-flex-row'}).find('span',attrs={'class':'a-size-medium a-text-bold'}).text

    except AttributeError:
        brand = ""	

    return brand


if __name__ == '__main__':
    
    
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.5'})
    
    URL = "https://www.amazon.in/s?k=sunscreen&crid=YOJT1WPRIYEQ&sprefix=sunscre%2Caps%2C739&ref=nb_sb_noss_2"
    
    #HTTP request
    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content,"html.parser")
   
    links = soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
    links_list = []
    
    #Loop for extracting links from tag objects
    for link in links:
        links_list.append(link.get('href'))
    
    d = {"title":[], "price":[], "brand":[], "rating":[], "reviews":[],"ingredients":[]}
    
    for link in links_list:
        try:
            new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
            #function calls to get required product information
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['brand'].append(get_brand(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['ingredients'].append(get_ingredients(new_soup))
            
        except: 
            continue
        
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df1 = amazon_df.drop_duplicates()
    amazon_df1.to_csv("amazon_data.csv", header=True, index=False)