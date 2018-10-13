text = open("./data/translations/fin.txt", encoding="utf8").read()

replace = [",", ".", "!", "?", "/", "&", "-", ":", ";", "@", "'", "...", '\n', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

import re
def multiple_replace(text, replace):
	rx = re.compile('|'.join(map(re.escape, replace)))
	return rx.sub('', text)

text = multiple_replace(text, replace)
text = text.lower()