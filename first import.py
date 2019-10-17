print('helloworld')
from bs4 import BeautifulSoup
import requests

baidu = requests.get('http://www.baidu.com').content
soul = BeautifulSoup(baidu,'html.parser')
links = soul.findAll('a')
for link in links:


    print(link.string)
'laalnad'
pull 
pull
