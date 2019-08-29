# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     level_2
   Description :
   Author :       pchaos
   date：          2019/8/30
-------------------------------------------------
   Change Activity:
                   2019/8/30:
-------------------------------------------------
"""

"""
Decrypt the following text 
Aipgsqi fego, xlmw pizip mw rsx ew iewc ew xli pewx fyx wxmpp rsx xss gleppirkmrk. Ws ks elieh erh irxiv xlmw teww: wlmjxxlexpixxiv
"""
from pycipher import Caesar

str = "Aipgsqi fego, xlmw pizip mw rsx ew iewc ew xli pewx fyx wxmpp rsx xss gleppirkmrk. Ws ks elieh erh irxiv xlmw teww: wlmjxxlexpixxiv"

for i in range(1,26):
	c = Caesar(key=i)
	print(c.decipher(str, keep_punct=True))

# letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
# for key in range(len(letters)):
# 	translated = ''
# 	translated = translated.upper()
# 	for symbol in str:
# 		if symbol in letters:
# 			num = letters.find(symbol)
# 			num -= key
# 			translated += letters[num]
# 		else:
# 			translated += symbol
# 	print("key #%s : %s" % (key, translated))


"""
result:
Welcome back, this level is not as easy as the last but still not too challenging. So go ahead and enter this pass: shiftthatletter
"""
