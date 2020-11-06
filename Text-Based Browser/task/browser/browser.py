import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

# write your code here
dir_name = "tb_tabs"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)


class Browser:

    def __init__(self):
        self.loaded_pages = deque()
        self.previous_page = self.loaded_pages

    def get_text_method(self, r):
        soup = BeautifulSoup(r, "html.parser")
        return soup.get_text()

    def back_method(self):
        if len(self.loaded_pages) == 0:
            return False
        elif len(self.loaded_pages) == 1:
            self.loaded_pages.pop()
            return False
        else:
            self.loaded_pages.pop()
            self.previous_page = self.loaded_pages[-1]
            return True

    def web_check(self):

        while True:
            user_input = input()
            if user_input == "exit":
                exit()
            elif user_input == "back":
                if self.back_method() is True:
                    print(self.previous_page)
                else:
                    self.web_check()
            elif ".com" not in user_input and ".org" not in user_input:
                print("Error: Incorrect URL")
                self.web_check()
            else:
                r = requests.get("https://{}".format(user_input))
                soup = BeautifulSoup(r.content, "html.parser")
                links = soup.find_all('a')
                for link in links:
                    print(Fore.BLUE + str(link.get('href')))
                file_name = user_input[:-4]
                loc = "{}\{}".format(dir_name, file_name)
                file = open(loc, "w+")
                    #  print(Fore.BLUE + str(link))
                file.write(soup.get_text())
                file.close()
                #  print(soup.get_text())
                self.loaded_pages.append(file_name)
                self.web_check()


    def file_check(self):

        while True:
            user_input2 = input()
            if "." in user_input2:
                self.web_check()
            elif user_input2 == "bloomberg":
                loc = "{}\{}".format(dir_name, user_input2)
                file = open(loc, "r")
                content = file.read()
                print(content)
                file.close()
                self.web_check()
            elif user_input2 == "nytimes":
                loc = "{}\{}".format(dir_name, user_input2)
                file = open(loc, "r")
                content = file.read()
                print(content)
                file.close()
                self.web_check()
            elif user_input2 == "exit":
                exit()


test = Browser()
test.web_check()
