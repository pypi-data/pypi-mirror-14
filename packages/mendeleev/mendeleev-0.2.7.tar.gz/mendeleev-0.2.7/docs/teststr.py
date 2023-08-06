# coding: utf-8
with open('data.rst', 'r') as f:
    data = f.read()
    
import codecs
codecs.ascii_decode(data)
