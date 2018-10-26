import os
import numpy as np
from xml.dom import minidom

res_dict = dict()

for doc in os.listdir(os.getcwd()):
	code = doc[5:-4]
	xmldoc = minidom.parse(doc)
	itemList = xmldoc.getElementsByTagName('udhr')
	if len(itemList) > 0:
		res_dict[code] = itemList[0].attributes['n'].value

np.save('OHCHR_decode.npy', res_dict)