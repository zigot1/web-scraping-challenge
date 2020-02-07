################################################
#### Set Scrapper
################################################
def Mars_scrape(db):
# Connect to a database. Will create one if not already available.
### Prerequisites
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import locale 

    import mimetypes
    
    import time
    from selenium import webdriver
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import NoSuchElementException
    

    #### Initiate Chrome
    
    ############################################
    ### Define Article scraper module
    ############################################
    def Articles_scraper(path):
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(10)
        driver.get(path)
        print("Artticle scraping started at path :", path)
        while True:
            try: 
                driver.find_element_by_xpath("""//*[contains(@class,'list_footer more_button')]""").click()
            except NoSuchElementException:
                break
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        teasers = driver.find_elements_by_class_name("article_teaser_body")
        titles  = driver.find_elements_by_class_name("content_title")
        dates = driver.find_elements_by_class_name("list_date")
        ## Generating List of Dictionaries - Mars Articles
        Mars_Articles_LIST = []
        for i in range(len(soup.find_all('div',class_='list_date'))):
            dict = {
                'date':dates[i].text,
                'title': titles[i].text,
                'article':teasers[i].text           
            }
            Mars_Articles_LIST.append(dict)
        driver.quit()
        return Mars_Articles_LIST
    ### End of Article Scrapping module
    #################################################################################
    ###
    #################################################################################
    ## Define Image Scrapping Module
    def Image_Scraper (path):
        print("Image Scraping module has started at path :", path)
        driver1 = webdriver.Chrome()
        driver1.set_page_load_timeout(10)
        driver1.get(path)
        driver1.find_element_by_xpath("""//*[contains(@id,'full_image')]""").click()
        driver1.maximize_window() ##For maximizing window
        driver1.implicitly_wait(5) ##gives an implicit wait for 20 seconds
        find_image = driver1.find_element_by_xpath("""//*[@id="fancybox-lock"]/div/div[1]/img""")
        featured_image = find_image.get_attribute('src')
        ###Confirm that Image has been Found
        print ("Image of the day :",featured_image)
        dict = {"img":featured_image}
        Mars_img_LIST = [dict]
        driver1.quit()
        return Mars_img_LIST
    ### End of Image Scrapping module
    ###################################################################################
    ###
    ####################################################################################
    ## Define Weather Tweeter Scrapping Module
    def Weather_Scraper (path):
        #url_w = 'https://twitter.com/marswxreport?lang=en'
        driver2 = webdriver.Chrome()
        driver2.get(path)
        driver2.maximize_window() ##For maximizing window
        driver2.implicitly_wait(5) ##gives an implicit wait for 20 seconds
        find_W_tweet = driver2.find_element_by_xpath("""//*[@id="react-root"]/div/div/div/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div/div[1]/div/article/div/div[2]/div[2]/div[2]/span""")
        print (find_W_tweet.text)
        Mars_Tweet = find_W_tweet.text
        driver2.quit()
        return Mars_Tweet
    ####################################################################################
    ###
    ####################################################################################
    ## Define Facts Scrapping Module
    def Mars_Facts(path):
        driver3 = webdriver.Chrome()
        driver3. get(path)
        driver3.maximize_window() ##For maximizing window
        driver3.implicitly_wait(5) ##gives an implicit wait for 20 seconds
        find_mars_facts = driver3.find_element_by_xpath("""//*[@id="tablepress-p-mars-no-2"]""")
                #### Some Fun
        table_elements = find_mars_facts.find_elements_by_tag_name("tr")
                ##### Nore Fun
        for element in table_elements:
            mtext = element.text
            print(mtext.split(':'))
                #### USe some bs4
        soup3 = BeautifulSoup(driver3.page_source, 'html.parser')
        table_holder = soup3.find('table')
                ###### Do some Pandas
        dfs_list = pd.read_html(str(table_holder))
                ###### Print Some Pandas
        for each in table_holder.contents:
            print(each.text)
        mars_dfs = dfs_list[0]
        mars_dfs.head()

        facts=[]
        for fact in (mars_dfs.to_dict('records')):
            print(fact[0], fact[1])
            dict = {"fact":fact[0], "data": fact[1]}
            facts.append(dict)
        driver3.quit()
        return facts
    ####################################################################################
    ## Define Images Scrapping Module
    def Mars_Big_Images (path):
        driver4 = webdriver.Chrome()
        driver4. get(path)
        #################
        ### Find and Click
        Mars_img_LIST = []
        for item in driver4.find_elements_by_xpath("""//*[@class='itemLink product-item' and contains(h3,'Enhanced')]"""):
            link = item.get_attribute('href')
            window_before = driver4.window_handles[0]
            driver4.execute_script("window.open(arguments[0])",link)
            window_after = driver4.window_handles[-1]
            driver4.switch_to.window(window_after)
            #Perform some action
            
            print(driver4.current_url)
            print(driver4.title.split('|')[0])
            original_image=driver4.find_elements_by_xpath("""//*[@id="wide-image"]/div/ul/li[2]/a""")
            link_image = original_image[0].get_attribute('href')
            print(link_image)
            dict = {'name': driver4.title.split('|')[0],
                    'page': driver4.current_url,
                    'img_url':original_image[0].get_attribute('href')}
            Mars_img_LIST.append (dict)
            driver4.switch_to.window(window_before)
        driver4.close()
        return Mars_img_LIST
    ####################################################################################
    ###                       END OF  MODULES                                       ####
    ####################################################################################
    ####
    ####
    ####
    ####################################################################################
    ##Populating Mongo Collection - Mars_Articles with the list of Dictionaries
    ####################################################################################
    if 'Mars_Articles' in db.list_collection_names():
        collection1 = db.Mars_Articles
        if collection1.estimated_document_count() == 0:
            ######Call Scraping Function
            print ('No Documents in Collection')
            Articles = Articles_scraper("https://mars.nasa.gov/news/")
            collection1.insert_many(Articles)
    else:  
        collection1 = db.create_collection("Mars_Articles")
        ######Call Scraping Function
        print ("Creating Collection")
        Articles = Articles_scraper("https://mars.nasa.gov/news/")
        collection1.insert_many(Articles)
       
    ###################################################################################
    ###################################################################################
    ### Get Mars Image of the day
    ###################################################################################
    print("IMAGE MODULE IS STARTING")
    if 'Mars_Image' in db.list_collection_names():
        collection_img = db.Mars_Image
    else:
        collection_img = db.create_collection("Mars_Image")
        collection_img.insert_many(Image_Scraper("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"))

    if collection_img.estimated_document_count() == 0:
        collection_img.insert_many(Image_Scraper("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"))
    ####################################################################################
    ####################################################################################
    #### MARS Weather
    ####################################################################################
    W_tweet = Weather_Scraper('https://twitter.com/marswxreport?lang=en')
    date_W =W_tweet.split(" ")[3]
    if 'Mars_Weather' in db.list_collection_names():
        collection_W = db.Mars_Weather
        if (collection_W.estimated_document_count() != 0) == True:
            last_entry = collection_W.find()
            if (date_W in list(last_entry[0].values())) == False:
                collection_W.insert_one({"date":date_W,"weather":W_tweet})
        else:
            collection_W.insert_one({"date":date_W,"weather":W_tweet})    
    else:
        collection_W = db.create_collection("Mars_Weather")
        collection_W.insert_one({"date":date_W,"weather":W_tweet})
    ##################################################################################
    ##################################################################################
    
    ####################################################################################
    #### MARS Data
    ####################################################################################
    if 'Mars_Data' in db.list_collection_names():
        collection_D = db.Mars_Data
        if (collection_D.find()) == False:
            collection_D.insert_many(Mars_Facts('https://space-facts.com/mars/'))
    else:
        collection_D = db.create_collection("Mars_Data")
        collection_D.insert_many(Mars_Facts('https://space-facts.com/mars/'))
    #################################################################################
    ######
    #################################################################################
   
    #################################################################################
    ##Populating Mongo Collection - Mars_Articles with the list of Dictionaries
    #################################################################################
    if 'Mars_Hemispheres' in db.list_collection_names():
        collection2 = db.Mars_Hemispheres
    else:
        collection2 = db.create_collection("Mars_Hemispheres")
    
    if collection2.count() == 0:
        collection2.insert_many(Mars_Big_Images ('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'))

print(__name__)