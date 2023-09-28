from selenium import webdriver
import os
import json
import time
import random
import datetime
import ctypes


class ChromeOptionsBuilder:
    """
    A class for building Chrome webdriver options.
    """
    @staticmethod
    def build_options():
        """
        Build Chrome webdriver options with specific configurations to prevent getting detected while using selenium.

        Returns:
            selenium.webdriver.chrome.options.Options: Chrome options object.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        return options


class InstagramLogin:
    """
    A class for handling Instagram login functionality.
    """
    @staticmethod
    def login(browser, username, password):
        """
        Log in to Instagram using the provided credentials.

        Args:
            browser (selenium.webdriver.chrome.webdriver.WebDriver): The WebDriver instance.
            username (str): Instagram username.
            password (str): Instagram password.
        """
        browser.get("https://www.instagram.com")
        username_field = browser.find_element_by_xpath("//input[@name='username']")
        password_field = browser.find_element_by_xpath("//input[@name='password']")

        time.sleep(random.uniform(1.0, 2.0))
        username_field.send_keys(username)
        time.sleep(random.uniform(1.0, 2.0))
        password_field.send_keys(password)
        time.sleep(random.uniform(1.0, 2.0))
        password_field.submit()
        time.sleep(5)
        browser.find_element_by_xpath("//button[text()='Log In']").click()


class InstagramBot:
    """
    A class representing an Instagram automation bot.
    """
    def __init__(self):
        """
        Initialize the InstagramBot instance.
        """
        self.browser = None
        self.j = -1
        self.error_counter = 0
        self.total_likes = 0
        self.like_counter = 0
        self.like_limit = 50
        self.sleep_time = 15  # minutes
        self.hashtags = ["fujifilm_xseries", "ig_romania", "bealpha", "fujifilm", "romania", "fujifilmxt30", "sonya7riii"]

        self.chrome_driver_path = os.environ.get('CHROME_DRIVER_PATH')
        if not self.chrome_driver_path:
            raise ValueError("CHROME_DRIVER_PATH environment variable not set.")

    def log(self, string):
        """
        Log a message with a timestamp.

        Args:
            string (str): The message to log.
        """
        print(str(datetime.datetime.now().hour).zfill(2) + ":" + str(datetime.datetime.now().minute).zfill(2) + " " + string)

    def open_browser(self):
        """
        Open a Chrome browser with configured options.
        """
        options = ChromeOptionsBuilder.build_options()
        self.browser = webdriver.Chrome(executable_path=self.chrome_driver_path, options=options)
        self.browser.delete_all_cookies()
        self.browser.implicitly_wait(10)

    def close_browser(self):
        """
        Close the Chrome browser if it's open.
        """
        if self.browser:
            self.browser.quit()

    def navigate_to_hashtag(self, hashtag):
        """
        Navigate to a specific hashtag on Instagram.

        Args:
            hashtag (str): The hashtag to navigate to.
        """
        self.browser.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        self.log(" Navigating to #" + hashtag + "...")

        try:
            self.browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button[1]").click()
        except:
            pass

    def like_image(self):
        """
        Like an image on Instagram.
        """
        try:
            time.sleep(random.uniform(2.0, 3.0))
            heart = self.browser.find_element_by_xpath("//button[@aria-label='Like']").click()
            value = heart.get_attribute("outerHTML").split("=")
            value = value[5].split("class")
            value = value[0].replace('"', "").strip()

            if value == "Like":
                heart.click()
                self.like_counter += 1
                self.log("Liking image. " + str(self.like_counter) + " liked images so far.")
                time.sleep(random.uniform(2.5, 4.0))
            else:
                self.log("image already liked. Skipping it. " + str(self.like_counter) + " liked images so far.")

            self.log("Next image.")
            self.browser.find_element_by_class_name("_65Bje").click()

        except Exception as e:
            print(str(e))
            self.log(str(self.like_counter) + " images liked. Going to the next hashtag due to an error encountered.")
            self.error_counter += 1

    def run(self):
        """
        Run the Instagram automation bot.
        """
        try:
            self.open_browser()
            with open('config.json', 'r') as f:
                config = json.load(f)
            InstagramLogin.login(self.browser, config['user']['name'], config['user']['password'])

            for _ in range(len(self.hashtags) * 4):
                self.total_likes += self.like_counter
                self.j += 1
                print("Total liked images so far: " + str(self.total_likes))

                if self.error_counter == 6:
                    self.log("Five errors encountered. Terminating session...")
                    break
                elif self.total_likes == 1500:
                    self.log("1500 likes done. Terminating session...")
                    break

                if self.j != 0:
                    self.log("Sleeping for " + str(self.sleep_time) + " minutes and closing the browser.")
                    self.close_browser()
                    time.sleep((self.sleep_time / 2) * 60)
                    self.log(str(self.sleep_time / 2) + " minutes left...")
                    time.sleep((self.sleep_time / 2) * 60)

                if self.j == len(self.hashtags):
                    self.j = 0

                self.navigate_to_hashtag(self.hashtags[self.j])
                self.like_counter = 0

                while self.like_counter < self.like_limit:
                    self.like_image()

            self.total_likes += self.like_counter
            self.log("Total images liked: " + str(self.total_likes))

        finally:
            self.close_browser()
            ctypes.windll.user32.MessageBoxW(0, "The script has been completed!", "Done", 0)


if __name__ == "__main__":
    bot = InstagramBot()
    bot.run()
