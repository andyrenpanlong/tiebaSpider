#coding=utf-8
import random
proxies=[
    'http://192.168.3.116:83',
    'http://192.168.3.116:8080',
    'http://192.168.3.116:80'
]

proxy={
    'http':proxies[random.randint(0,len(proxies)-1)]
}