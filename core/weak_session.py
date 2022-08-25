import datetime
import hashlib
from selenium import webdriver


class SESSION(object):

  cookie = {'domain':'172.17.0.2','httponly':False,'name':'PHPSESSID','value':'24nr5an77p46e52bipuv7luv12','path':'/','secure':False}
  driver = webdriver.PhantomJS()

  def __init__(self,url,cookies):
    self.url = url
    self.cookies = cookies

  def session(self):
    self.POST_SESSION()
    self.URL()

  def POST_SESSION(self):
    for key in self.cookies:
      self.cookie['name'] = key
      self.cookie['value'] = self.cookies[key]
      self.driver.add_cookie(self.cookie)

  def URL(self):

    while True:
      self.driver.get(self.url)
      self.driver.find_element_by_tag_name("input").click()
      print("\033[1;32mSESSION Generate!\033[0m")
      cookies = self.driver.get_cookies()

      for key in cookies:
        if "dvwaSession"  == key['name']:
          session = self.driver.get_cookie("dvwaSession")
          name = session['name']
          value = session['value']
          print(name,": ",value)
          if self.cookies['security'] == "medium":
            timestamp = int(value)
            value = datetime.datetime.fromtimestamp(timestamp)
            print("Type is unix time stamp")
            print("\033[1;33mDecode Value\033[0m",name," : ",end='')
            print(f"{value:%Y-%m-%d %H:%M:%S}")
          elif self.cookies['security'] == 'high':
            print("Type is md5 hashing asymmetric algorithm")
            count = 0
            while True:
              md5 = hashlib.md5(str(count).encode())
              if md5.hexdigest() == value:
                print("\033[1;33mMD5 Value Find %s \033[0m" % str(count))
                break
              count += 1

          elif self.cookies['security'] == 'low':
            print("Type Is Base number")

      q = input("press q to quit:")
      if q == 'q':
        self.driver.delete_all_cookies()
        self.driver.quit()
        break

