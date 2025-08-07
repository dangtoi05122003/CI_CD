from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from config import setup
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service
from database import MONGO_URI,MONGO_DB,MONGO_COLLECTION
'''
import sys
sys.tracebacklimit = 0
'''
class main(webdriver.Chrome):
    def __init__(self):
        options = setup()
        service = Service(executable_path="/usr/bin/chromedriver")
        super(main, self).__init__(service=service, options=options)


        #self.maximize_window()
        sleep(5)
    def website(self):
        self.set_page_load_timeout(150)
        self.get("https://e.vnexpress.net/")
    def database(self):
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        self.collection = db[MONGO_COLLECTION]
    def trend(self):
        self.implicitly_wait(15)
        Col_topnews = self.find_element(By.CSS_SELECTOR, '.col-left-topstory.flexbox')
        item_topnews = Col_topnews.find_elements(By.CLASS_NAME, 'item-topstory')
        for item in item_topnews:
            try:
                title = item.find_element(By.CLASS_NAME, "title_news_site").text
            except:
                title = None
            try:
                description = item.find_element(By.CLASS_NAME, "lead_news_site").text
            except:
                description = None
            try:
                img_tag = item.find_element(By.CLASS_NAME, "thumb_size").find_element(By.TAG_NAME, "img")
                image_url = img_tag.get_attribute("src")
            except:
                image_url = None
            if not title and not description and not image_url:
                continue  
            data = self.collection.find_one({'title': title})
            if data:
                if not data.get("img") and image_url:
                    self.collection.update_one(
                        {'_id': data['_id']},
                        {'$set': {'img': image_url}}
                    )
            else:
                document = {
                    "title": title,
                    "description": description,
                    "img": image_url
                }
                self.collection.insert_one(document)


            print("Title:", title)
            print("Description:", description)
            print("Image:", image_url)
            print("-" * 50)
if __name__ =='__main__':
    app = main()
    try:
        app.website()
        app.database()
        app.trend()
    finally:
        app.quit()
