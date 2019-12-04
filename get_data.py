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

# def init_browser():
#     driver = webdriver.Chrome('/Users/rachel_roundtree/Desktop/chromedriver\ 2') #download from here, https://chromedriver.chromium.org/downloads and use the path
#     return driver
def init_browser():
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = "http://localhost:8888"
    prox.ssl_proxy = "http://localhost:8888"
    
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)
    
    options = webdriver.ChromeOptions()
    options.binary_location = '/Users/rachel_roundtree/Desktop/chromedriver\ 2'
    # options.add_argument('headless')
    # set the window size
    options.add_argument('window-size=1881x1280')
    
    # initialize the driver
    driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)
    return driver

def searches_lists(driver, collections):
    search_trend_urls = ['https://trends.google.com/trends/yis/' + year + '/US/' for year in collections]
    # search_trend_urls = ['https://trends.google.com/trends/yis/2008/US/']
    
    for each_year in search_trend_urls:
        time.sleep(2)
        driver.get(each_year)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="anchorName"]/div/div/div[2]/div[1]')))
        buttons = driver.find_elements_by_xpath('//*[@id="anchorName"]/div/div/div[2]/div[1]')
        
        for b in buttons:
            driver.execute_script("arguments[0].click();", b)
        
        collection = re.sub('(https:\/\/trends.google.com\/trends\/yis\/)', '', each_year[:-4])    
        each_lists = driver.find_elements_by_class_name('grid-cell')
        container = []

        for each in each_lists:
            each_category = {}
            each_list = []
            ranking = each.find_elements_by_class_name('fe-expandable-list-question-index')
            keyword = each.find_elements_by_class_name('fe-expandable-item-text')

            each_category['year'] = collection
            each_category['category'] = each.find_element_by_tag_name('span').text

            for i in range(len(ranking)):            
                each_keyword = {}       
                each_keyword['ranking'] = ranking[i].text
                each_keyword['keyword'] = keyword[i].text
                each_keyword['href'] = keyword[i].get_attribute('href')
                each_list.append(each_keyword)
            
            each_category['rank_keyword'] = each_list
            container.append(each_category)
        
        result = keywords_contents(driver, container)
        print('result: ', result)

        for each_key in result:
            collections[collection].insert_many([
                { 'year' : each_key['year'],
                'category' : each_key['category'],
                'ranking' : each_infos['ranking'],
                'keyword' : each_infos['keyword'],
                'href' : each_infos['href'],
                'related_queries' : each_infos['related_queries'],
                'image_url' : each_infos['image_url']
            } for each_infos in each_key['rank_keyword']])

        # [{'categoty': each_key['category'], 'name': each_infos['keyword']} for each_key in result for each_infos in each_key['rank_keyword']]
       
    return

def keywords_contents(driver, container):
    for each_category in container:
        for each_keyword in each_category['rank_keyword']:
            driver.get(each_keyword['href'])     
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div')))
            time.sleep(1)          
            # if driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/ng-include/div/div[1]/div/ng-include/a/div/div[2]/span') == False:                                                                     # /html/body/div[2]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/ng-include/div                
            try:                                                                                            
                if 'has-error' in WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/ng-include/div'))).get_attribute('class'):
                    each_keyword['related_queries'] = ''
                else:
                    if ', ' in each_keyword['keyword']:                              
                        each_keyword['related_queries'] = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/md-content/div/div/div[5]/trends-widget/ng-include/widget/div/div/ng-include/div/div[1]/div/ng-include/a/div/div[2]/span'))).text
                    else:                                                                                                            
                        each_keyword['related_queries'] = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/ng-include/div/div[1]/div/ng-include/a/div/div[2]/span'))).text
            except Exception as e:
                print(each_keyword['keyword'])
                each_keyword['related_queries'] = ''
                pass

            params = {
            "q" : each_keyword['keyword'] + ' ' + each_keyword['related_queries'],
            "num" : 1,
            "start" : 1,
            "imgSize" : "medium",
            "searchType" : "image",
            "filetype" : "png",
            "cx" : "001842575000215983116:kinu75kosuy",
            "key" : "AIzaSyDpg6bq6O6aQOl_Dpfd2RmAbQGPmM2qgGM"
            }

            response = requests.get('https://www.googleapis.com/customsearch/v1', params = params, stream=True)
            img_src = json.loads(response.text)
            each_keyword['image_url'] = img_src['items'][0]['link']
    return container

def access_db(dbname, collectionnames):
    cluster = MongoClient('mongodb+srv://rimho:0000@cluster0-yehww.mongodb.net/test?retryWrites=true&w=majority')
    db = cluster[dbname]
    collections = {c:db[c] for c in collectionnames}
    return db, collections

def main():
    db, collections = access_db('google_search_db', [ '2011', '2012', '2013', '2014', '2016', '2017', '2018'])
    driver = init_browser()
    time.sleep(3)
    searches_lists(driver, collections)
    print('Go To MongoDB')
    return 

main()




