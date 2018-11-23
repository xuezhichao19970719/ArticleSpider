# -*- coding: utf-8 -*-
import  hashlib


def get_md5(url):
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    return  md5.hexdigest()

if __name__ == '__main__':
    print(get_md5('http://blog.jobbole.com/114496/'))