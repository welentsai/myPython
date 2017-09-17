# -*- coding: utf-8 -*-

# The format specifier {:>4} means “print this argument right-justified within 4 spaces.”
# with statement close file automatically after its code block end
line_number = 0
with open('favorite-people.txt', encoding='utf-8') as a_file:
	for a_line in a_file:
		line_number += 1
		print('{:>4} {}'.format(line_number, a_line.rstrip()))         


# mode = 'w' => 覆寫(overwriting )模式 
# \r => a carriage return => 回到行首
# \n =>  a line feed => 跳下一行, 
# 在 Windows 的換行是 "\r\n", 在 Unix 系列的換行是 "\n"
# 行尾加 \r 或 \n 在python內都可以
with open('test.log', mode='w', encoding='utf-8') as a_file:
	a_file.write('test log ok2\r')
	a_file.write('test log ok2\n')
	a_file.write('test log ok2\n')


# mode='a' => append mode
with open('test.log', mode='a', encoding='utf-8') as a_file:
	a_file.write('test log append\r')
	a_file.write('test log append\r')