"""
This is the print_rec.py module and it provides one function called print_rec()
which prints lists that may or may not include nested lists.
"""
def print_rec(li,indent=False , level=0,fh = sys.stdout):
	"""
		This function takes a positional arguments called 'li',which is 
		any Python list( of - possibly - nested lists).Each data item in		the provided list is (recursively) printed to the screen on it's		own line. A second argument called 'indent' controls whether or 		not indentation is shown on the display.This defaults to False:
		set it to True to switch on.A third argument called 'level' (whi		ch defaults to 0)is used to insert tab-stops when a nested list 		is encountered.A forth argument caled 'fh'(which defaults to sys		.stdout) is used to choose whether print the data to a file or 
		screen.	"""
        for each_item in li:
                if isinstance(each_item,list):
                        print_rec(each_item,indent,level+1,fh)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print('\t',end='',file=fh)
                        print(each_item,file=fh)
