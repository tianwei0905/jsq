import sys
import csv
import json

##chu li canshu lei
class Arges(object):
	def __init__(self,arges):
		self.arges = arges
		self.conf_name = self.get_filename('-c')
		self.src_name = self.get_filename('-d')
		self.out_name = self.get_filename('-o')		
 
	def get_filename(self,canshu):
		index = self.arges.index(canshu)
		file_name = self.arges[index+1]
		return file_name

##config file class
class conf(object):
	def __init__(self,file_name):
		self.file_name = file_name
		self.conf_data = self.open_file(file_name)
	def open_file(self,conf_name):
		self.conf_name = conf_name
		with open(self.conf_name,'r') as file:
			conf_dict = {}
			for line in file:
				line = 	line.split('=')
				dict_key = line[0].strip()
				dict_val = line[1].strip() 
				conf_dict[dict_key] = dict_val
			return conf_dict

##user data class
class userdata(object):
	def __init__(self,user_file):
		self.user_file = user_file
		self.user_data = self.return_user(user_file)
	def return_user(self,user_file):
		with open(self.user_file,'r') as file:
			user_dict = {}
			line_len = 0
			for line in file:
				line = line.split(',')
				dict_key = line[0]
				dict_val = line[1]
				user_dict[dict_key] = dict_val
				return user_dict

if __name__ == '__main__':
	arges = Arges(sys.argv[1:])
	conf_file = arges.conf_name
	src_file = arges.src_name
	out_file = arges.out_name
	conf_data = conf(conf_file).conf_data

	for key,value in conf_data.items():
		print(key,value)
	
	user_data = userdata(src_file).user_data
