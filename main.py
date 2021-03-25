from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys

class user_prefs():

    def ask_save_path(self):
        save_path = input("Enter full path to save location. Leaving this blank will save the files to the Downloads folder\n")
        if save_path:
            self.save_path = save_path
        else:
            self.save_path = None

    def ask_res_y(self):
        self.res_y = input("Enter vertical resolution\n")

    def ask_res_x(self):
        self.res_x = input("Enter horizontal resolution\n")

    def ask_wp_count(self):
        try:
            self.wp_count = int(input("Enter how many wallpapers you want to download. (Must be a positive number)\n"))
        except:
            print("Please enter a valid number")

    def ask_url(self):
        url = input("Enter url to preferred /r/wallpapers feed. Blank for default (top weekly)\n")
        if url:
            self.url = url
        else:
            self.url = None

if __name__ == '__main__':

    user_prefs = user_prefs()
    user_prefs.ask_save_path()
    user_prefs.ask_res_x()
    user_prefs.ask_res_y()
    user_prefs.ask_wp_count()
    user_prefs.ask_url()

    if user_prefs.url:
        url = user_prefs.url
    else:
        url = "https://www.reddit.com/r/wallpapers/top/?t=week"

    # configure chromedriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    if user_prefs.save_path:
        download_directory = user_prefs.save_path
        pref = {'download.default_directory': f"{download_directory}"}
        chrome_options.add_experimental_option('prefs', pref)

    # opens r/wallpapers, scrolls to the bottom 3 times
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    for i in range(1, 3):
        print("Scrolling to bottom")
        driver.execute_script("window.scrollTo(1,50000)")
        print("Waiting for the page to load")
        time.sleep(5)
    time.sleep(5)
    file = open('r-wallpapers.txt', 'w')
    write = str((driver.page_source).encode('utf-8'))
    file.write(write)
    file.close()
    driver.close()

    # get all a tags
    soup = bs(open('C:/Users/Tolga/PycharmProjects/wallpaperbot/r-wallpapers.txt'), 'html5lib')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    # get the links that take you to comments
    wallpapers = []
    for link in links:
        try:
            if 'reddit.com/r/wallpapers/comments' in link:
                wallpapers.append(link)
        except TypeError:
            continue

    # get the download link from each page
    paperlinks = []
    driver = webdriver.Chrome(options=chrome_options)
    for wallpaper in wallpapers:
        try:
            print(f"Searching for the ze-robot link for {wallpaper}")
            driver.get(wallpaper)
            soup = bs(driver.page_source.encode('utf-8'), 'html5lib')
            found = False
            for a in soup.find_all('a'):
                if f'{user_prefs.res_x}×{user_prefs.res_y}' in a:
                    paperlinks.append(a.get('href'))
                    found = True
                    break
            if not found:
                print(f"Couldn't find ze-robot link  for {wallpaper}")
        except:
            continue

    # write download links to file
    with open('wallpaper-links.txt', 'w') as file:
        for link in paperlinks:
            file.write(str(link) + '\n')

    downloaded = 0
    # open each link one by one and download
    with open('wallpaper-links.txt') as file:
        while True:
            try:
                driver.get(file.readline())
                print("Done")
                downloaded += 1
            except:
                break
    driver.close()
    print(f"Found links for {len(wallpapers)} wallpapers, found downloads for {len(paperlinks)}, downloaded {downloaded} of them.")

    sys.exit()