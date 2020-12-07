# Bot
from config import details
from config import comments
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import sys
import time
import random
import pyautogui as pg
from tkinter import *
import threading
from alert import send_alert


# Create bot class
class InstaBot:

    # Init
    def __init__(self, username, password):
        """
        Initializes an instance of the InstaBot class.
        Call the login method to authenticate a user with IG.

        Args:
            username:str: Instagram username
            password:str: Instagram password

        Attributes:
            driver:Selenium.webdriver.Chrome: The Chromedriver used to automate browser actions

        """
        # Some variables
        self.username = username
        self.password = password
        self.base_url = "https://www.instagram.com/"
        self.number_of_comments = len(comments)
        self.log = "Click \'Login\' to start bot."

        # Probabilities (1 in [x] chance)
        self.prob_like = 5      # 20%
        self.prob_follow = 50   # 2%
        self.prob_comment = 10  # 10%

        # Create path variable for driver
        self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.MAC_PATH = "/Users/bradegbert/Documents/chromedriver"
        self.RP_PATH = "/usr/bin/chromedriver"

        # Start program
        self.open_gui()

    # GUI
    def open_gui(self):
        # Initialize GUI
        self.gui = Tk()
        self.gui.title("Instabot")
        self.gui.geometry("350x500")
        self.gui.resizable(width=False, height=False)
        self.gui.configure(bg="black")

        # Create labels
        label_title = Label(
            self.gui, text="InstaBot", font='none 24 bold', fg="white", bg="#DD2A7B")

        label_madeby = Label(
            self.gui, text="made by Brad Egbert", font='none 10', fg="gray", bg="black")

        label_log = Label(self.gui, text=self.log,
                          font='none 12', fg="#FEDA77", bg="black")

        # Create login thread
        # Set daemon to true so thread can end
        login_thread = threading.Thread(target=self.login)
        login_thread.daemon = True
        login_botless_thread = threading.Thread(target=self.login_botless)
        login_botless_thread.daemon = True

        # Create buttons
        # Login will start a new thread (process) so that GUI doesn't freeze
        button_login = Button(self.gui, text="Login", font='none 16 bold', width=15, height=2,
                              fg="white", bg="#F58529", command=login_thread.start)

        button_login_botless = Button(self.gui, text="Login (No Bot)", font='none 16 bold', width=15, height=2,
                                      fg="white", bg="#F58529", command=login_botless_thread.start)

        button_quit = Button(self.gui, text="Quit", font='none 16 bold',
                             width=15, height=2, fg="white", bg="#515BD4", command=self.quit_program)

        # Pack everything
        label_title.pack(fill=BOTH, pady=20)
        button_login.pack(pady=20)
        button_login_botless.pack(pady=20)
        button_quit.pack(pady=20)
        label_log.pack(pady=20)
        label_madeby.pack(pady=5, fill=BOTH)

        self.gui.mainloop()

    # Login
    def login(self):
        # Create webdriver
        self.driver = webdriver.Chrome(self.RP_PATH)

        # Goes to URL page using string interpolation ... '{}' is the self.base_url
        # For example '{}/accounts/login'.format(self.base_url) would go to https://www.instagram.com/accounts/login
        self.driver.get('{}'.format(self.base_url))
        time.sleep(2)
        print("Logging in...")

        # Find fields and login
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[3]').click()
        time.sleep(3)

        # Close login notification
        print("Closing notifications...")
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(2)

        # Close notification
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[3]/button[2]').click()

        print("Starting...")
        time.sleep(2)
        self.reset()

    # Login
    def login_botless(self):
        # Create webdriver
        self.driver = webdriver.Chrome(self.PATH)

        # Goes to URL page using string interpolation ... '{}' is the self.base_url
        # For example '{}/accounts/login'.format(self.base_url) would go to https://www.instagram.com/accounts/login
        self.driver.get('{}'.format(self.base_url))
        time.sleep(2)
        print("Logging in...")

        # Find fields and login
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[3]').click()
        time.sleep(3)

        # Close login notification
        print("Closing notifications...")
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(2)

        # Close notification
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[3]/button[2]').click()

        print("Logged in successfully!")

    # Refresh current page
    def refresh_page(self):
        print("Refreshing page...")
        self.driver.refresh()
        time.sleep(4)

    # Return current url
    def get_current_url(self):
        return self.driver.current_url

    # Choose an action at random
    def do_something(self):

        # Either browse page, scroll on page, or reset
        if self.choose_three() == 0:
            self.browse_posts()
        elif self.choose_three() == 1:
            self.nav_explore()
        else:
            self.scroll_down()
            self.browse_posts()

    # Returns either 0 or 1
    def choose(self):
        c = random.randint(0, 1)
        return c

    # Returns either 0, 1 or 2
    def choose_three(self):
        c = random.randint(0, 2)
        return c

    # Go to explore page
    def reset(self):
        self.nav_explore()

    # Sleep a short amount of time
    def sleep_short(self):
        ss = random.randint(5, 10)
        time.sleep(ss)

    # Sleep for a random amount of time
    def sleep_random(self):
        sr = random.randint(15, 45)
        print("Sleeping for " + str(sr) + " seconds...")
        time.sleep(sr)

    # Scroll to bottom of the page
    def scroll_down(self):
        print("Scrolling down...")
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)")
        self.sleep_short()

    # Quit program
    def quit_program(self):
        print("Quitting program...")
        self.gui.destroy()
        self.driver.quit()
        sys.exit(0)

    # Go to explore page
    def nav_explore(self):
        print("Navigating to explore page...")
        self.driver.get('{}{}/'.format(self.base_url, 'explore'))
        time.sleep(4)

        # Chance to refresh explore page
        if self.choose_three() == 0:
            self.refresh_page()
            self.sleep_short()

        # Chance to scroll before collecting post links
        if self.choose() == 0:
            self.scroll_down()
            self.sleep_short()

        self.do_something()

    # Go to user page
    def nav_user(self, user):
        # Go to user page
        # Same thing as self.driver.get('https://instagram.com/user/')
        print("Navigating to " + user + "\'s page...")
        self.driver.get('{}{}/'.format(self.base_url, user))
        print("Success!")

    # Follow user
    def follow_user(self, user):
        # Go to user page
        print("Attempting to follow " + user + "...")
        self.nav_user(user)
        time.sleep(1)
        try:
            follow_button = self.driver.find_elements_by_xpath(
                "//button[contains(text(), 'Follow')]")[0]
            follow_button.click()
            print("Success!")
        except:
            print("Unable to locate follow button.")
            pass

    # Unfollow user
    def unfollow_user(self, user):
        # Go to user page
        print("Attempting to unfollow " + user + "...")
        self.nav_user(user)
        time.sleep(1)
        try:
            unfollow_button = self.driver.find_element_by_class_name('_5f5mN')
            unfollow_button.click()
            unfollow_confirm = self.driver.find_element_by_xpath(
                "//button[contains(text(), 'Unfollow')]")
            unfollow_confirm.click()
            print("Success!")
        except:
            print("Unable to locate unfollow button.")
            pass

    # Search by hashtag
    def search_hashtag(self, hashtag):
        # Search hashtag
        print("Searching by hashtag #" + hashtag + "...")
        search = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search.send_keys('#' + hashtag)
        time.sleep(2)
        # Click hashtag
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]/div/div').click()
        print("Success!")
        time.sleep(2)

    # Returns all post links on current page
    def get_post_links(self):
        # Finds all elements with href (links)
        links = self.driver.find_elements_by_xpath('//*[@href]')
        post_links = []

        # For each element found, check if it has a post url and if so, add it to post_links array
        for l in links:
            if "https://www.instagram.com/p/" in l.get_attribute('href'):
                post_links.append(l.get_attribute('href'))

        time.sleep(1)
        return post_links

    # Like posts on current page
    def browse_posts(self):
        print("Retrieving valid POST links...")
        post_links = self.get_post_links()
        post_links_count = len(post_links)
        print("Navigating to post...")

        # Attempt to like post
        def attempt_like():
            chance_to_like = random.randint(1, self.prob_like)

            try:
                # Try to click like, otherwise reset
                like = self.driver.find_element_by_class_name('fr66n')

                if chance_to_like == 1:
                    like.click()
                    print("Liked post! ❤")
                    self.sleep_short()
                else:
                    print("Did not like post! ❌")
                    self.sleep_short()
            except:
                print("Unable to like post!")
                self.sleep_short()

        # Attempt to follow poster
        def attempt_follow():
            chance_to_follow = random.randint(1, self.prob_follow)

            try:
                # Try to click follow, otherwise reset
                follow = self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button')

                if chance_to_follow == 1:
                    follow.click()
                    print("Followed poster! ❤")
                    self.sleep_short()
                else:
                    print("Did not follow poster! ❌")
                    self.sleep_short()
            except:
                print("Unable to follow poster!")
                self.sleep_short()

        # Attempt to comment on post
        def attempt_comment():
            chance_to_comment = random.randint(1, self.prob_comment)

            # Generates a random index of comments array
            num = random.randint(0, self.number_of_comments - 1)
            time.sleep(1)

            # Attempt to comment
            try:
                # Find comment box
                comment_box = self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea')
                send = self.driver.find_element_by_xpath(
                    "//button[contains(text(), 'Post')]")

                x = comment_box.location.get('x') + 32
                # Works at 150 for Windows, must be 190 for RaspberryPi
                y = comment_box.location.get('y') + 190

                if chance_to_comment == 1:
                    print("Commenting on post! ❤")
                    print(comments[num])

                    # Send alert via email
                    send_alert("Commented on a post!",
                               f"{comments[num]}\n\n{self.get_current_url()}", "bradegbert26@gmail.com")

                    # Comment with pyautogui
                    pg.moveTo(x, y, 0.25)
                    time.sleep(2)
                    pg.click()
                    time.sleep(1)
                    pg.typewrite(comments[num], 0.02)
                    time.sleep(1)

                    send.click()
                    self.sleep_short()
                else:
                    print("Did not comment on post! ❌")
                    self.sleep_short()
            except:
                print("Unable to comment on post!")
                self.sleep_short()

        # Loop through posts
        for p in range(0, post_links_count):
            # Go to posts & like
            self.driver.get(post_links[p])
            print("Pretending to be human... 💤")
            self.sleep_short()
            # Attempt like/comment/follow
            attempt_like()
            attempt_follow()
            attempt_comment()

        # Clear links list and reset
        post_links.clear()
        self.reset()


# Run bot
if __name__ == "__main__":

    bot = InstaBot(details["email"], details["password"])
