from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import csv
import string


class WebCleaner(object):

    def __init__(self, text):
        self.text = text
    # This price cleans the data and returns placeholders
    # if all the data isn't filled out correctly

    def split_text(self):
        text = self.text.replace('\n', ' ')
        text = text.replace("'/'", '')
        text.replace(':', ' ')
        out = text.split(' ')
        try:
            if '29"' in out:
                condition = out[5]
                if '-' in out:
                    size = out[11]
                    wheel_size = out[14]
                    material = out[15]
                    if 'Carbon' in out:
                        front_travel = out[17]
                        rear_travel = out[21]
                    else:
                        front_travel = out[16]
                        rear_travel = rear_travel[20]
                else:
                    size = out[8]
                    wheel_size = out[11]
                if "Carbon" in out:
                    material = out[13]
                    front_travel = out[17]
                    rear_travel = out[21]
                else:
                    material = out[13]
                    front_travel = out[16]
                    rear_travel = out[20]
            elif '27.5"' in out:
                condition = out[5]
                size = out[8]
                wheel_size = out[11]
                if "Carbon" in out:
                    material = out[15]
                    front_travel = out[19]
                    rear_travel = out[23]
                else:
                    material = out[15]
                    front_travel = out[18]
                    rear_travel = out[22]
            if ('29"' not in out) and ('27.5"' not in out):
                return ['invalid', 'data', 'condition',
                        'these', 'are', 'placeholers']
        except BaseException:
            return ['invalid', 'data', 'condition',
                    'these', 'are', 'placeholers']
        return [condition, size, wheel_size,
                material, front_travel, rear_travel]

    def clean_price(self):
        # This function will clean the price data of the website
        exclude = set(string.punctuation)
        s = ''.join(ch for ch in self.text if ch not in exclude)
        out = s.split(' ')
        return out


def scraping_func():
    # Loop through each page on the website
    for x in range(1, 2):
        first_url = 'https://www.pinkbike.com/buysell/list/'
        second_part_url = f'?region=3&page={x}&category=2'
        url = first_url + second_part_url
        driver.get(url)
        # On Each page there are 20 postings to scrape data from.
        for i in range(1):
            print(i * '.')
            read_more_button = driver.find_elements_by_xpath(
                        "(//b[contains(.,'[Read More]')])")
            sleep(1)
            # click each post

            read_more_button[i].click()
            # find all the data on each post

            title = [driver.find_element_by_xpath(
                '//*[@id="content-container"]/div/h1').text.replace(',', ' ')]
            desc = driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[1]/div[1]/div[2]/div[1]')
            price = driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[1]/div[2]/div')
            cleaned_desc = WebCleaner(desc.text)
            cleaned_price = WebCleaner(price.text)
            title_cleaned = title + cleaned_desc.split_text()
            write_data = title_cleaned + cleaned_price.clean_price()
            # write data to CSV file

            f.write(','.join(write_data))
            f.write('\n')

            sleep(1)
            driver.back()
    driver.close()
    f.close()


if __name__ == '__main__':
    # The following loads the personal data
    # that helps make the scaping proccess faster
    dir_Galv = '/home/devin/Documents/Galvanize/'
    dir_repo = 'repos/Galvanize_Capstone_1/'
    fire_prof = 'data/firefoxprofile'
    profile = webdriver.FirefoxProfile(dir_Galv + dir_repo + fire_prof)
    driver = webdriver.Firefox(firefox_profile=profile)
    # Write the Columns of the CSV file
    f = open('data3.csv', 'w')
    headers_1 = 'Title,Condition,Size,Wheel_Size,'
    headers_2 = 'Material,Front_travel,Rear_travel,Price,Currance'
    f.write(headers_1 + headers_2)
    f.write('\n')
    # The Scraping function could be cleaner but I don't have the time
    scraping_func()
    print('connection is closed')
