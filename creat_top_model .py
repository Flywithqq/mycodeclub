import os
import re
import datetime
from tkinter import *
from tkinter.filedialog import *

def creat_tb(fp):
	t1=datetime.datetime.now()
	now=t1.strftime("%Y-%m-%d %H:%M:%S")
	fp.write("//generate time is "+now+"\n")
	fp.write('''
/************************************************************\\
 **  Copyright (c) 2011-2017 Anlogic, Inc.\n
 **  All Right Reserved.\n
\************************************************************/
''')
	fp.write("//author is xxx \n")
	fp.write("//revision is x.y.z \n")
	fp.write('''
module top_model ( );

''')
	#fp2=open("run.bat","w")
	#fp2.write("vsim.exe -do run.do")
	

def find_portlist(fp,iotype):
	global top_fp
	global uut_tb
	global Mname
	port_list=[]
	strs=iotype+"\s+(reg|wire)?(\s)?(?P<width>\[.*\])?(\s)?(?P<portname>.*);"
	#strs=iotype+"\s+(reg|wire)?(\s)?(?P<width>\[.*\])?(\s)?(?P<portname>.*);"
	input_pat=re.compile(strs)
	for line in fp:
		modulename="module\s+(?P<MODULE>[\w]+)\s?\(?.*"
		i=re.search(modulename,line)
		if i:
			Mname=i.group("MODULE")
			print("module name is {}".format(Mname))
		
		a=re.search(input_pat,line)
		if a:
			if (iotype=="input"):  ## judge port type
				b=a.group("portname").split(',') ## multiple input pin in one line
				if type(b) == type([]):
					if a.group("width") :
						for i in b:
							port_list.append(i)
							#top_fp.write("reg "+a.group("width")+" "+i+";\n")
							uut_tb.append( " . "+i+" ( "+ i + "),")
							
					else:
						for i in b:
							port_list.append(i)
							#top_fp.write("reg "+i+";\n")	
							uut_tb.append( " . "+i+" ( "+ i + "),")
							
				else: ## one input pin in one line
					port_list.append(b)
					#top_fp.write("reg ".join(b).join(";\n"))
					uut_tb.append(" . " + b + "(" + b + "),")
				
			if (iotype=="output"):
				b=a.group("portname").split(',')
				if type(b) == type([]):
					if a.group("width") :
						for i in b:
							port_list.append(i)
							#top_fp.write("wire "+a.group("width")+" "+i+";\n")
							uut_tb.append( " . "+i+" ( "+ i + "),")
					else:
						for i in b:
							port_list.append(i)
							#top_fp.write("wire "+i+";\n")
							uut_tb.append( " . "+i+" ( "+ i + "),")	
				else:
					port_list.append(b)
					#top_fp.write("wire ".join(b).join(";\n"))
					uut_tb.append(" . " + b + "(" + b + "),")
	print( iotype+" port list is :{}".format(port_list))
		
	fp.seek(0,0)
	return port_list
	
def creat_uut_tb (fp,inst,port_i,port_o): ## io is list type 
	uut=" inst_"+inst
	fp.write(inst+ uut+" (\n")
	for a in port_i:
		print("port i is {}".format(a))
		fp.write(" ." + a + "(" + a + "),\n")
	for i,j in enumerate (port_o):
		print("port o is {}".format(j))
		if (i== (len(port_o)-1)):
			fp.write(" ." + j + "(" + j + ")\n);\n")
		else:
			fp.write(" ." + j + "(" + j + "),\n")
		
def add_initial (fp):
	fp.write('''
initial begin // need add
	
	
end//end initial 
endmodule
	''')
def add_endmodule(fp):
	fp.write("endmodule \n")

def find_vfile_list():
	vfilelist=askopenfilenames(filetypes=[("all v files",".v")])	
	#print("select  vfile is {}".format(vfile))
	#vdir,vfile=os.path.split(vfile)
	return vfilelist
	
def main():
	## you only need select top.v and will generate top_tb.v
	global top_fp
	global uut_tb
	global Mname
	vfilelist=find_vfile_list()
	uut_tb=[]
	top_fp=open("top_module.v","w")
	creat_tb(top_fp) 
	for vfile in vfilelist:
		vdir,vname=os.path.split(vfile)
		vn,vext=os.path.splitext(vname)
		fp=open(vfile,"r")
	
	
		port_i=find_portlist(fp,"input")
		port_o=find_portlist(fp,"output")
		creat_uut_tb(top_fp,Mname,port_i,port_o)
		#print(" port i is {}".format(port_i))
		#add_initial(top_fp)
		fp.close()
	add_endmodule(top_fp)
	top_fp.close()
	
if __name__=='__main__':
	main()
	#exit(input())
	