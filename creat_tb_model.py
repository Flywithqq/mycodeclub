###rev0.0  creat by qqzhang 2017.7.20
###rev0.1 add inout port detect

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
	fp.write("//author is qqzhang \n")
	fp.write("//revision is x.y.z \n")
	fp.write('''
`timescale 1ns/100ps
module tb();
''')
	fp2=open("run.bat","w")
	fp2.write("vsim.exe -do run.do")
	

def find_portlist(fp,iotype):
	global tb_fp
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
							tb_fp.write("reg "+a.group("width")+" "+i+";\n")
							uut_tb.append( " . "+i+" ( "+ i + "),")
							
					else:
						for i in b:
							port_list.append(i)
							tb_fp.write("reg "+i+";\n")	
							uut_tb.append( " . "+i+" ( "+ i + "),")
							
				else: ## one input pin in one line
					port_list.append(b)
					tb_fp.write("reg ".join(b).join(";\n"))
					uut_tb.append(" . " + b + "(" + b + "),")
				
			if (iotype=="output"):
				b=a.group("portname").split(',')
				if type(b) == type([]):
					if a.group("width") :
						for i in b:
							port_list.append(i)
							tb_fp.write("wire "+a.group("width")+" "+i+";\n")
							uut_tb.append( " . "+i+" ( "+ i + "),")
					else:
						for i in b:
							port_list.append(i)
							tb_fp.write("wire "+i+";\n")
							uut_tb.append( " . "+i+" ( "+ i + "),")	
				else:
					port_list.append(b)
					tb_fp.write("wire ".join(b).join(";\n"))
					uut_tb.append(" . " + b + "(" + b + "),")
					
			if (iotype=="inout"):
				b=a.group("portname").split(',')
				if type(b) == type([]):
					if a.group("width") :
						for i in b:
							port_list.append(i)
							tb_fp.write("wire "+a.group("width")+" "+i+";\n")
							uut_tb.append( " . "+i+" ( "+ i + "),")
					else:
						for i in b:
							port_list.append(i)
							tb_fp.write("wire "+i+";\n")
							uut_tb.append( " . "+i+" ( "+ i + "),")	
				else:
					port_list.append(b)
					tb_fp.write("wire ".join(b).join(";\n"))
					uut_tb.append(" . " + b + "(" + b + "),")		
		
	print( iotype+" port list is :{}".format(port_list))
		
	fp.seek(0,0)
	return port_list
	
def creat_uut_tb (fp,inst,port_i,port_o,port_io=None): ## io is list type 
	fp.write(inst+ " uut_tb (\n")
	for a in port_i:
		print("port i is {}".format(a))
		fp.write(" ." + a + "(" + a + "),\n")
	if "port_io" :
		for a in port_io:
			print("port io is {}".format(a))
			fp.write(" ." + a + "(" + a + "),\n")
		
	for i,j in enumerate (port_o):
		print("port o is {}".format(j))
		if (i== (len(port_o)-1)):
			fp.write(" ." + j + "(" + j + ")\n);")
		else:
			fp.write(" ." + j + "(" + j + "),\n")
		
def add_initial (fp):
	fp.write('''
initial begin // need add
	
	
end//end initial 
endmodule
	''')

def find_vfile():
	vfile=askopenfilename(filetypes=[("all v files",".v")])	
	#print("select  vfile is {}".format(vfile))
	#vdir,vfile=os.path.split(vfile)
	return vfile
	
def main():
	## you only need select top.v and will generate top_tb.v
	vfile=find_vfile()
	vdir,vname=os.path.split(vfile)
	vn,vext=os.path.splitext(vname)
	fp=open(vfile,"r")
	global tb_fp
	global uut_tb
	global Mname
	uut_tb=[]
	vtb=vn+"_tb.v"
	tb_fp=open(vtb,"w")
	creat_tb(tb_fp)
	port_i=find_portlist(fp,"input")
	port_o=find_portlist(fp,"output")
	port_io=find_portlist(fp,"inout")
	creat_uut_tb(tb_fp,Mname,port_i,port_o,port_io)
	#print(" port i is {}".format(port_i))
	add_initial(tb_fp)
	
	
if __name__=='__main__':
	main()
	#exit(input())
	