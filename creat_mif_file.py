import  os 
import string
import random
from tkinter import *

##output type is string eg input 4,8 and output 00000100
def decimal2target(num,width,target="bin"): 
	if (target.upper()=="BIN" ):
		a=bin(num)
		alenth=len(a)
		activelen=alenth-2
		if activelen<width :
			b=(width-activelen)*"0"+a[2:]
			result=b
			print("input num is {},width is {},result {} is {}".format(num,width,target,result))
		else:
			result=a[2:]
			print("input num is {},width is {},result {} is {}".format(num,width,target,result))
	
	
	elif (target.upper()=="OCT" ):
		a=oct(num)
		alenth=len(a)
		activelen=alenth-2
		if activelen<width :
			b=(width-activelen)*"0"+a[2:]
			result=b
			print("input num is {},width is {},result {} is {}".format(num,width,target,result))
		else:
			result=a[2:]
			print("input num is {},width is {},result {} is {}".format(num,width,target,result))
	
	
	elif (target.upper()=="HEX" ):
		a=hex(num)
		alenth=len(a)
		activelen=alenth-2
		if activelen<width :
			b=(width-activelen)*"0"+a[2:]
			result=b
			print("input num is {},width is {},result {} is {}".format(num,width,target,result))
		else:
			result=a[2:]
			print("input num is {},width is {},result {} is {}".format(num,width,target,result))
	return result
	
## verilog data <={data[6:0],data[7]^data[0]}	
## verilog data[n:0] <={data[n-1:0],data[n]^data[0]}
def shift_l(strings,num):
	i=0
	while (num>0):
		lsb=int(strings[0]) ^int(strings[len(strings)-1])
		strings=strings[1:]+str(lsb)
		num=num-1
		print("after shift is {}".format(strings))
		fp.write("{} : {} ;\n".format(bin(i),strings))
		i=i+1
	fp.write("END;")
	return strings
	
def shift(strings,num):
	i=[]
	while (num>0):
		lsb=int(strings[0]) ^int(strings[len(strings)-1])
		strings=strings[1:]+str(lsb)
		num=num-1
		print("after shift is {}".format(strings))
		i.append(int(strings,2))
		
	return i

def creat_mif_file(fp,depth=64,width=8,addr_r="HEX",data_r="HEX"):
	fp.write('''% multipe-line comment
	multiple-line comment %\n''')
	fp.write("--single-line comment\n")
	fp.write("DEPTH = {};\n".format(depth))
	fp.write("WIDTH = {};\n".format(width))
	
	fp.write("ADDRESS_RADIX = {};\n".format(addr_r.upper()))
	fp.write("DATA_RADIX = {};\n".format(data_r.upper()))
	
		
	fp.write("\n")
	fp.write("CONTENT\n")
	fp.write("BEGIN\n")
	
def addr_gen(start,end,direction="up",step=1):
	addr=[]
	i=start
	if (direction=="up" or direction=="UP"):
		while (i<=end):
			addr.append(i)
			print("count up addr is {}".format(i))
			i=i+step
	if (direction=="down" or direction=="DOWN"):
		while(i>=end):
			addr.append(i)
			print("count down addr is {}".format(i))
			i=i-step
	print("addr list is {}".format(addr))
	return addr
def gen_random(start,end,num):
	result=[]
	while (num>0):
		a=random.randint(start,end)
		result.append(a)
		num=num-1
	return result
		

def writedata(fp,addr,data,width,addr_r,data_r):
	num=1
	for i in zip (addr,data):
		if (addr_r.upper()=="HEX"):
			addr2=decimal2target(i[0],width,"hex")
		if (addr_r.upper()=="OCT"):
			addr2=decimal2target(i[0],width,"oct")
		if (addr_r.upper()=="BIN"):
			addr2=decimal2target(i[0],width,"bin")
		if (addr_r.upper()=="UNS"):
			addr2=i[0]
			
		if (data_r.upper()=="HEX"):
			data2=decimal2target(i[1],width,"hex")
		if (data_r.upper()=="OCT"):
			data2=decimal2target(i[1],width,"oct")
		if (data_r.upper()=="BIN"):
			data2=decimal2target(i[1],width,"bin")
		if (data_r.upper()=="UNS"):
			data2=i[1]
				
		line=str(addr2) +"	:	" + str(data2)+"	;"
		linecomment="	--this is {} th data in mem \n".format(num) 
		num=num+1
		fp.write(line+linecomment)
		
		
	
	fp.write("END;")
class creat_gui(object):
	
	def creat_top():
		top=Tk()
		top.title("creat mem initial file with mif type")
	def get_entry(inst):
		pass
		
		
if __name__ == '__main__' :
	fp=open("ram1k_9.mif","w")
	DEPTH=1024
	WIDTH=9
	ADDR_R="bin"
	DATA_R="bin"
	##decimal to bin/hex/oct width eg when small and will output it is
	DATA_W=1 
	
	creat_mif_file(fp,depth=DEPTH,width=WIDTH,addr_r=ADDR_R,data_r=DATA_R)
	addr=addr_gen(0,1023,"up",1)
	data=addr_gen(0,511,"up",1)
	data2=shift("1111111",1024)
	data3=gen_random(1,500,512)
	data4=data + data3
	writedata(fp,addr,data4,DATA_W,ADDR_R,DATA_R)
	