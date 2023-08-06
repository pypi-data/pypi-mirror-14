""" 这个模块主要功能是，将一个文件进行读取，读取后的内容保存至一个列表，再调用ListPrint模块，
对列表中的内容进行分句处理，最后输出到一个新的文本文档中"""

import ListPrint

man = []
other =[]

try:
	data = open('sketch.txt')

	for each_line in data:
		try:
			(role,line_spoken) = each_line.split(':',1)
			line_spoken = line_spoken.strip()
			if role == 'Man':
				man.append(line_spoken)
			elif role == 'Other Man':
				other.append(line_spoken)
		except ValueError:
			pass
	data.close()
except IOError as err:
	print("File Error: " + str(err))

try:
	with open('man_file.txt','w') as man_file:
		ListPrint.print_list(man,location = man_file)
	with open('other_file.txt','w') as other_file:
		ListPrint.print_list(other,location = other_file)

except IOError as with_err:
	print('File Error: ' + str(with_err))