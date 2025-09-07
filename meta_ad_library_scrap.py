import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


from bs4 import BeautifulSoup



def extract_countries_with_bs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    countries = set()
    
    # Find all table cells in the first column (aria-colindex="1")
    country_cells = soup.find_all('td', {'aria-colindex': '1'})
    
    for cell in country_cells:
        country_div = cell.find('div', class_='x1yrsyyn')
        if country_div:
            countries.add(country_div.text.strip())
    
    return sorted(list(countries))





def scrap_meta_ad_library(url, ad_id):
    url = f"{url}{ad_id}"  # Construct 
    resp = driver.get(url)
    # if response.status_code != 200:
    #     print(f"Failed to retrieve page for ad ID {ad_id}. Status code: {response.status_code}")
    #     return

    try:
        # Find the button element with XPath
        see_ad_detail_btn_xpath = '//*[@id="facebook"]/body/div[5]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div'

        # Wait until the button is clickable
        see_ad_detail_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, see_ad_detail_btn_xpath))
        )
        
        #print(see_ad_detail_btn)
    
        see_ad_detail_btn.click()
        found = True

        transparency_by_location_btn_x_path = '//*[contains(text(), "Transparency by location")]'
        transparency_by_location_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, transparency_by_location_btn_x_path))
        )
        transparency_by_location_btn.click()
        #get the age element 
        age_xpath = '//*[contains(text(), "years old")]'
        age_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, age_xpath))
        )
        print(age_element.text)

        #get gender element 

        #get location element
        # location_xpath = '//*[@id="facebook"]/body/div[6]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[2]/div[3]/div[3]/div[2]/div[1]/div/table/tbody'
        # location_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, location_xpath))
        # )
        #print(location_element.get_attribute("outerHTML"))

        #locations = extract_countries_with_bs(location_element.get_attribute("outerHTML"))
        #print(locations)  # Print 

        #Get the list of locatiions 
        
        #gender_xpath = '//*[@id="facebook"]/body/div[6]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[2]/div[5]/div[2]'
        #gender_element = WebDriverWait(driver, 10).until(
        #EC.presence_of_element_located((By.XPATH, gender_xpath))
        #    )
        #print(gender_element.text)
       # print([age_element.text, gender_element.text, locations])
        #return [age_element.text, gender_element.text, locations], found
        return [age_element.text], found

    except:
        print(f"Error clicking button or finding element for ad ID {ad_id}.")



if __name__ == "__main__":
    options = Options()
    options.add_argument("--start-maximized")   # open browser maximized
    options.add_argument("--disable-notifications")  # disable popups
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    nb_matched_ads = 0
    nb_ads = 0
    #df_instagram = pd.read_csv('data/targeting_categories/instagram_data_with_targeting_categories_granularity.csv')
    #df_instagram = df_instagram[df_instagram['advertisement.details.advert_id'].notna()]
    #df_fb = pd.read_csv('data/targeting_categories/facebook_data_with_targeting_categories.csv')
    #df_fb = df_fb[df_fb['advertisement.details.advert_id'].notna()]
    df_fb = pd.read_csv('fb_ad_library.csv')
    for index, row in df_fb.iterrows():
        if isinstance(row['selected_ad_library'],str):
            continue
        ad_id = int(row['advertisement.details.advert_id'])
        if len(str(ad_id)) > 15:
            continue
        try:
            taregting_elements, ad_match = scrap_meta_ad_library("https://www.facebook.com/ads/library/?id=", ad_id)
            if ad_match:
                nb_matched_ads +=1
        except:
            continue
        df_fb.at[index, 'selected_ad_library'] = str(taregting_elements)

print(f"{nb_matched_ads} out of {nb_ads} was macthed")
df_fb.to_csv('fb_ad_library_non_detecetd.csv', index=False)
    

