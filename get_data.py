from selenium import webdriver
# 1st import: Allows you to launch/initiate a browser
from selenium.webdriver.common.by import By
# 2nd import: Allows you to search for things using specific parameters.
from selenium.webdriver.support.ui import WebDriverWait
# 3rd import: Allows you to wait for a page to load.
from selenium.webdriver.support import expected_conditions as EC
# 4th import: Specify what you are looking for on a specific page in order to determine that the webpage has loaded.
from selenium.common.exceptions import TimeoutException
# 5th import: Handling a timeout situation
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType

import re, pymongo, time, pdb, itertools, requests, json
from pymongo import MongoClient

def init_browser():
    # driver = webdriver.Chrome('/Users/hh/Documents/ECT/rimhoho.github.io/chromedriver')
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = "http://localhost:8118"
    prox.ssl_proxy = "http://localhost:8118"
    
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)
    
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    # options.add_argument('headless')
    # set the window size
    options.add_argument('window-size=1881x1280')
    
    # initialize the driver
    driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)
    return driver

def searches_lists(driver, collections):
    base_url = 'https://trends.google.com/trends/yis/'
    years = ['2014', '2015', '2016', '2017', '2018']
    search_trend_urls = [base_url + year + '/' + country + '/' for country in collections for year in years]
    # search_trend_urls = ['https://trends.google.com/trends/yis/2018/PK/']
    
    for each_country in search_trend_urls:
        time.sleep(2)
        driver.get(each_country)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="anchorName"]/div/div')))
        buttons = driver.find_elements_by_xpath('//*[@id="anchorName"]/div/div/div[2]/div[1]')
        
        for b in buttons:
            driver.execute_script("arguments[0].click();", b)
        
        collection = each_country[-3:-1]  
        year = re.sub('(https:\/\/trends.google.com\/trends\/yis\/)', '', each_country[:-4])
        each_lists = driver.find_elements_by_class_name('grid-cell')
        container = []

        for each in each_lists:
            each_category = {}
            each_list = []
            ranking = each.find_elements_by_class_name('fe-expandable-list-question-index')
            keyword = each.find_elements_by_class_name('fe-expandable-item-text')

            each_category['country'] = collection
            each_category['category'] = each.find_element_by_tag_name('span').text

            for i in range(len(ranking)):            
                each_keyword = {}       
                each_keyword['ranking'] = ranking[i].text
                each_keyword['keyword'] = keyword[i].text
                each_keyword['href'] = keyword[i].get_attribute('href')
                each_list.append(each_keyword)
            
            each_category['rank_keyword'] = each_list
            container.append(each_category)

        result = get_higher_search_by_region(driver, container)

        collections[collection].insert_many([
            { 'country' : each_key['country'],
              'year' : year,
              'category' : each_key['category'],
              'ranking' : each_infos['ranking'],
              'keyword' : each_infos['keyword'],
              'href' : each_infos['href'],
              'region' : each_searches['region'],
              'search_volume' : each_searches['search_volume']
        } for each_key in result for each_infos in each_key['rank_keyword'] for each_searches in each_infos['higher_search_volumes']])
        print('result: ', result)
    return

def get_higher_search_by_region(driver, container):
    for each_category in container:
            for each_keyword in each_category['rank_keyword']:
                driver.get(each_keyword['href'])     
                each_list = []
                time.sleep(3)                    
                try:
                    interest_lists = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div/div[2]/widget/div')))
                    for item in interest_lists.find_elements_by_class_name('progress-label'):
                        search_volume = item.find_element_by_class_name('progress-value').text
                        if int(search_volume) > 49:
                            each_dict = {}
                            region = item.find_element_by_class_name('label-text').find_element_by_tag_name('span').text
                            each_dict['region'] = region
                            each_dict['search_volume'] = search_volume
                            each_list.append(each_dict)
                    each_keyword['higher_search_volumes'] = each_list
                except Exception as e:
                    print('error', each_keyword['keyword'])
                    each_keyword['higher_search_volumes'] = ''
                    pass
    return container

def access_db(dbname, collectionnames):
    cluster = MongoClient('mongodb+srv://rimho:0000@cluster0-yehww.mongodb.net/test?retryWrites=true&w=majority')
    db = cluster[dbname]
    collections = {c:db[c] for c in collectionnames}
    return db, collections

def main():
    db, collections = access_db('3_Google_search_trends_db', ['IN'])
    driver = init_browser()
    time.sleep(3)
    searches_lists(driver, collections)
    print('Go To MongoDB')
    return 

main()

