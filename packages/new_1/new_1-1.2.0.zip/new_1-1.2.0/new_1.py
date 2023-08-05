movies = ["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,["Graham Chapman",
				["Michael Palin","John Cleese","Terry Gilliam","Eric Idle","Terry Jones"]]]

				
def print_out_V1(text_list,indent=False,table=0):
	for each_item in text_list:
		if isinstance(each_item,list):
			print_out_V1(each_item,indent,table+1)
		else:
			if indent:
				for num in range(table):
					print("\t",end="")
			
			print(each_item)	


		
def print_out(text_list):
	for each_item in text_list:
		if isinstance(each_item,list):
			print_out(each_item)
		else:
			print(each_item)
			