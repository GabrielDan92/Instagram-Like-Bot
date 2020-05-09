from selenium import webdriver
import os, json, time, random, datetime, ctypes

# change the working directory to target the json file
os.chdir("C:\\Users\\user\\Desktop\\programming\\Python")

def openChrome():
    # add settings to prevent getting detected using selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")
    #options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # open the browser
    browser = webdriver.Chrome(executable_path=r"C:\Users\user\Desktop\programming\chromedriver.exe", options=options)
    browser.delete_all_cookies()
    browser.implicitly_wait(10)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})

    # open the json file containing the username and password
    with open('config.json','r') as f:
        config = json.load(f)

    # log in
    browser.get("https://www.instagram.com")
    username = browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input")
    password = browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input")
    time.sleep(random.uniform(1.0, 2.0))
    username.send_keys(config['user']['name'])
    time.sleep(random.uniform(1.0, 2.0))
    password.send_keys(config['user']['password'])
    time.sleep(random.uniform(1.0, 2.0))
    password.submit()

    # check if the Instagram pop up exists and click on it if it does
    try:
        browser.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]").click()
    except:
            print("Pop up not found")

    return browser
#==============================================================================================

j = -1
errorCounter = 0
totalLikes = 0
likeCounter = 0
likeLimit = 50
sleepTime = 10 #minutes

def log(string):
    print(str(datetime.datetime.now().hour).zfill(2) + ":" + str(datetime.datetime.now().minute).zfill(2) + " " + string)

hshtgList = ["fujifilm_xseries", "ig_romania", "bealpha", "fujifilmxt30", "romania", "sonya7riii"]

for i in range(len(hshtgList) * 3):
    totalLikes += likeCounter
    j += 1
    print("Total liked images so far: " + str(totalLikes))

    if errorCounter == 6:
        log("Five errors encountered. Terminating session...")
        break
    elif totalLikes == 1050:
        log("1000 likes done. Terminating session...")
        break

    if j != 0:
        log("Sleeping for " + str(sleepTime) + " minutes and closing the browser.")
        browser.quit()
        time.sleep((sleepTime/2) *60)
        log(str(sleepTime/2) + " minutes left...")
        time.sleep((sleepTime/2) *60)

    if j == len(hshtgList):
        j = 0

    browser = openChrome()
    browser.get("https://www.instagram.com/explore/tags/" + hshtgList[j] + "/")
    log(" Navigating to #" + hshtgList[j] + "...")

    # click on the first image
    browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div").click()
    likeCounter = 0

    while True:
        if likeCounter == likeLimit:
            log(str(likeLimit) + " liked images. Moving to the next hashtag.")
            break
        try:
            time.sleep(random.uniform(2.0, 3.0))

            # retrieve the heart attribute (Liked/Do not like)
            heart = browser.find_element_by_class_name("wpO6b").find_element_by_css_selector("svg:first-child") 
            value = heart.get_attribute("outerHTML").split("=")
            value = value[1].split("class")
            value = value[0].replace('"', "").strip()

            # like the picture if it's not already liked, based on the attribute retrieved above
            if value == "Like":
                heart.click()
                likeCounter += 1
                log("Liking image. " + str(likeCounter) + " liked images so far.")
                time.sleep(random.uniform(2.0, 3.0))
            else:
                log("image already liked. Skipping it. " + str(likeCounter) + " liked images so far.")

            log("Next image.")
            browser.find_element_by_class_name("_65Bje").click()

        except:
            log(str(likeCounter) + " images liked. Going to the next hashtag due to error encountered.")
            errorCounter += 1
            break

totalLikes += likeCounter
log("Total images liked: " + str(totalLikes))
log("Quiting browser...")
browser.quit()
ctypes.windll.user32.MessageBoxW(0, "The script has been completed!", "Done", 0)
