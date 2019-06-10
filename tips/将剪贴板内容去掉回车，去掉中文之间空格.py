# -*- coding: utf-8 -*-
import pyperclip, re
txtsrc = pyperclip.paste()
reReturn = re.compile(r'\r|\n|\r\n')
reSpcBetwnChnChara = re.compile(r'([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])')
txtsrc = re.sub(reReturn,'',txtsrc)
txtsrc = re.sub(reSpcBetwnChnChara,r'\1\2',txtsrc)

dict_key = r"１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ，．／！＠＃＄％＾＆＊（）＜＞？；＇：｛｝＿＋－＝"
dict_val = r"1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,./!@#$%^&*()<>？;':{}_+-="
dict_ = {}
reQuanjiao = re.compile(r'[{0}]'.format(dict_key))
for i in range(len(dict_key)):
    dict_[dict_key[i]]=dict_val[i]
dict_['＂']='"'

def quanjiao2banjiao(mo):
    c = mo.group(0)
    return dict_[c]

txtsrc = re.sub(reQuanjiao,quanjiao2banjiao,txtsrc)
print(txtsrc)
pyperclip.copy(txtsrc)
