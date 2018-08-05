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
		user_csv = csv.reader(open(user_file,'r'))	
		user_dict = {}
		for line in user_csv:
			dict_key = line[0]
			dict_val = line[1]
			user_dict[dict_key] = dict_val
		return user_dict
		user_file.close()

##ji suan gong zi class
class  mingxi(object):
	def __init__(self,weage,conf_dict):
		self.weage = float(weage)
		self.conf_dict = conf_dict
		if self.weage <= float(self.conf_dict['JiShuL']):
			self.weage = self.conf_dict['JiShuL']
		elif self.weage >= float(self.conf_dict['JiShuH']):
			self.weage = self.conf_dict['JiShuH']
		else:
			self.weage = self.weage
		weage_base = float(self.weage)
		self.shebao_pay = self.shebao(weage_base)
	def shebao(self,weage_base):
		self.weage_base = weage_base
		self.yanglao = self.weage_base * float(self.conf_dict['YangLao'])
		self.yiliao = self.weage_base * float(self.conf_dict['YiLiao'])
		self.shiye = self.weage_base * float(self.conf_dict['ShiYe'])
		self.gongshang = self.weage_base * float(self.conf_dict['GongShang'])
		self.shengyu = self.weage_base * float(self.conf_dict['ShengYu'])
		self.gongjijin = self.weage_base * float(self.conf_dict['GongJiJin'])
		self.shebao_pay = self.yanglao + self.yiliao + self.shiye + self.gongshang + self.shengyu + self.gongjijin
		return	format(self.shebao_pay,'.2f')

##ji suan jiao shui
class tax(object):
	def __init__(self,tax_money):
		self.tax_money = tax_money
		self.tax_pay = self.tax_pay(tax_money)
	def tax_pay(self,tax_money):
		tax_base = self.tax_money - 3500
		if tax_base <= 0:
			tax_pay = 0
		elif tax_base <=1500:
			tax_pay = tax_base * 0.03 - 0
		elif tax_base <= 4500:
			tax_pay = tax_base * 0.1 - 105
		elif tax_base <= 9000:
			tax_pay = tax_base * 0.2 - 555
		elif tax_base <= 35000:
			tax_pay = tax_base * 0.25 - 1005
		elif tax_base <= 55000:
			tax_pay = tax_base * 0.3 - 2755
		elif tax_base <= 80000:
			tax_pay = tax_base * 0.35 - 5505
		else:
			tax_pay = tax_base * 0.45 - 13505
		return format(tax_pay,'.2f')

##write to csv
class w_csv(object):
	def __init__(self,w_data,file_name):
		self.w_data = w_data
		self.w_file = file_name
		w_out = self.w_to(self.w_data,self.w_file)
	def w_to(self,w_data,w_file):
			open_w = open(w_file,'a',newline='')
			csv_w = csv.writer(open_w)
			csv_w.writerow(w_data)
			open_w.close()

		

if __name__ == '__main__':
	arges = Arges(sys.argv[1:])
	conf_file = arges.conf_name
	src_file = arges.src_name
	out_file = arges.out_name
	conf_data = conf(conf_file).conf_data
#	print(conf_data['JiShuL'])

#	for key,value in conf_data.items():
#		print(key,value)
	
	user_data = userdata(src_file).user_data
#	print(user_data)
	
#	test = mingxi(16444,conf_data).shebao_pay
#	print(test)
	
#	test1 = tax(5000).tax_pay
#	print(test1)
	for key,value in user_data.items():
		user_sq = user_data[key]
		user_sb = mingxi(user_sq,conf_data).shebao_pay
		user_jse = float(user_sq) - float(user_sb)
		user_js = tax(user_jse).tax_pay 
		user_sh = float(user_sq) - float(user_sb) - float(user_js)
		user_sh = format(user_sh,'.2f')
		user_data_out = (key,user_sq,user_sb,user_js,user_sh)
		w_csv(user_data_out,out_file).w_to
