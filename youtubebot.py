#This is a youtube Bot that is able to view a video,and eventually add views on youtube videos
#Code cheza kiwewe
#Tested and works on Windows Machine.
"""Author : X
   ©2021 David Mugalla"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import re
from bs4 import BeautifulSoup
from time import sleep

URL = input("Enter valid URL of Youtube Video  >begin with 'https://' \n ")

logging.basicConfig(filename='Botlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

page  = requests.get(URL)

def viewAction(soup, duration_seconds):
    viewCounter = 0
    ans = input("Is this the video you want to get more views : y or n ? ")
    newViews = int(input("How many views would you like to add? "))
    if (ans=='y'):
        logging.warning("========== Starting Bot Activity ==========")
        
        while(viewCounter<newViews):
            ChromeOptions = Options()
            ChromeOptions.headless = True
            
            browser = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), 
                options=ChromeOptions
            )
            browser.get(URL)
            browser.implicitly_wait(10)
            
            try:
                WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Play']"))).click()
                print("---------------------")
                print("Video has started playing "+ "\U0001F910")
                print("---------------------")
                logging.info("Video has started playing")
                
                # Sleep dynamic video timing without pafy dependency
                print(f"Watching for {duration_seconds} seconds...")
                sleep(duration_seconds)
                    
            except Exception as e:
                logging.error(f"An error occurred during video runtime: {e}")

            viewCounter+=1
            print("---------------------")
            print("Video has finished playing "+ "\U0001F619")
            print("---------------------")
            print("---------------------")
            print("Added a total of "+ str(viewCounter) + " view(s)")
            print("---------------------")
            browser.close()
            
            if(viewCounter==newViews-1):
                for view in soup.findAll('div',attrs={'class':'watch-main-col'}):
                    finalview = view.find("meta", itemprop="interactionCount")['content']
                    print(f"final view Count : " + finalview + "\n")
                    logging.info("final view Count : " + finalview + "\n")

            sleep(2)
    else:
        print("Terminating Activity")
        exit(-1)


def vidScrapper(page):
    soup = BeautifulSoup(page.content,"html.parser")
    regex = re.compile(r'^(http(s)??\:\/\/)?(www\.)?((youtube\.com\/watch\?v=)|(youtu.be\/))([a-zA-Z0-9\-_])+')

    duration_seconds = 45 # Default standard watch time fallback

    if regex.match(URL):
        try:
            print("Valid URL\n")
            logging.info("Found information about video")

            print("\n     ==============================================      \n")
            for info in soup.findAll('div',attrs={'class':'watch-main-col'}):
                title  = info.find("meta", itemprop="name")["content"]
                print(f"Title of Video : " + title + "\n")
                logging.info(title)

            for date in soup.findAll('div',attrs={'class':'watch-main-col'}):
                date = date.find("meta",itemprop="datePublished")["content"]
                print(f'Date Published :' + date + "\n")
                logging.info('Date :' + date + "\n")
            
            for view in soup.findAll('div',attrs={'class':'watch-main-col'}):
                view = view.find("meta", itemprop="interactionCount")['content']
                print(f"Initial view Count : " + view + "\n")
                logging.info("Initial view Count : " + view + "\n")
            
            for desc in soup.findAll('div',attrs={'class':'watch-main-col'}):
                desc = desc.find("meta", itemprop="description")['content']
                print(f"Description : " + desc + "\n")
                logging.info("Description : " + desc + "\n")
            
            # Scrapes ISO duration tag (ex: PT4M15S) to figure out watch time completely offline
            duration_meta = soup.find("meta", itemprop="duration")
            if duration_meta:
                iso_time = duration_meta['content']
                nums = [int(x) for x in re.findall(r'\d+', iso_time)]
                if 'H' in iso_time and 'M' in iso_time and 'S' in iso_time:
                    duration_seconds = nums[0]*3600 + nums[1]*60 + nums[2]
                elif 'M' in iso_time and 'S' in iso_time:
                    duration_seconds = nums[0]*60 + nums[1]
                elif 'S' in iso_time:
                    duration_seconds = nums[0]
                elif 'M' in iso_time:
                    duration_seconds = nums[0]*60
    
            print("\n     ==============================================      \n")
            
        except Exception as e:
            logging.error(f"An Error occurred while finding the video: {e}")
            exit(-1)
    else :
        print("Invalid URL please enter a valid Youtube Video URL")
        exit(-1)
       
    return viewAction(soup, duration_seconds)

if __name__ == "__main__":
    logging.info('Starting program')
    vidScrapper(page)
