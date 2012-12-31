import xml.etree.cElementTree as etree

tree = etree.parse("level.oel")
root = tree.getroot()
stringMap = root.findtext("NewLayer0")

v = 0
for i in stringMap:
	if i == '1':
		v+=1
		print(v)