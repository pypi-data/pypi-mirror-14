''' matrix function '''
def matrix_display(data,cols):
	if cols<=1 or cols>len(data)/2:
		print ("Unable to convert to matrix.")
		return
	if not len(data) % cols==0:
		print ("Cannot convert to Matrix")
		return
	if not len(data) % 2 == 0:
		print ("Unable to Convert odd number of items into a Matrix")
	else:
		for index,item in enumerate(data):
			if index%cols==0:
				print('')
				print(item,end='')
			else:
				print('\t',end='')
				print(item,end='')
				
				


			