#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  treemap.py
#  
#  Phu Dang
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import csv
import operator
import datetime

def createCsvFile(key_word,data):
	today = datetime.date.today()
	with open('increased_order_'+key_word+str(today)+'.csv','wb') as written_file:
		file_writer = csv.writer(written_file)
		for i in range(2):
			file_writer.writerow([x[i] for x in data])
	
def main():
	data = {}
	first_line = True
	key_word = ""
	with open('Consumer_Complaints.csv','rb') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if first_line == True:
				key_word = row[8]
			if row[8] != "" and first_line == False:
				if not data.has_key(row[8]):
					data.update({row[8]:1})
				else:
					data[row[8]] = data[row[8]]+1
			first_line = False
	sort_data = sorted(data.items(),key=operator.itemgetter(1),reverse=True)
	createCsvFile(key_word,sort_data)	
	return 0

if __name__ == '__main__':
	main()

