import os
import sys
import re

def clean_text(text):
        cleaned_text = re.sub('[a-zA-Z]', '', text)
        cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', \
                '', cleaned_text)
        return cleaned_text

f = open('usd.txt', 'r')

info = f.readline()
info_list = info.split(' ')

dollar = info_list[0]
weight = info_list[1]
date = info_list[2]

log1 = open('currency_log.txt', 'a')
log2 = open('currency_log2.txt', 'a')

date = clean_text(date[:-1])

#print(date)

log1.write('\n')
log1.write(dollar)
log1.write(', ')
log1.write(weight)

log2.write('\n')
log2.write(date)
log2.write(', ')
log2.write(dollar)
