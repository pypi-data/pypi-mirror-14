import json
class IdentyNumber(object):
	"""This tool can help you  verify Taiwanese identy number .
		if the number is invalid ,then you will get the return 'False' """ 
	def __init__(self):
		self.code_rule = [
			['A',10,'台北市'],
			['B',11,'台中市'],
			['C',12,'基隆市'],
			['D',13,'台南市'],
			['E',14,'高雄市'],
			['F',15,'台北縣'],
			['G',16,'宜蘭縣'],
			['H',17,'桃園縣'],
			['I',34,'嘉義市'],
			['J',18,'新竹縣'],
			['K',19,'苗栗縣'],
			['L',20,'台中縣'],
			['M',21,'南投縣'],
			['N',22,'彰化縣'],
			['O',35,'新竹市'],
			['P',23,'雲林縣'],
			['Q',24,'嘉義縣'],
			['R',25,'台南縣'],
			['S',26,'高雄縣'],
			['T',27,'屏東縣'],
			['U',28,'花蓮縣'],
			['V',29,'台東縣'],
			['W',32,'金門縣'],
			['X',30,'澎湖縣'],
			['Y',31,'陽明山'],
			['Z',33,'連江縣'],
			]
	def get_rules(self):
		return json.dumps(self.code_rule)

	def __isValid(self, id_num):
		city_letter = id_num[0:1]
		if not id_num[1:].isdigit() or len(id_num) != 10:
			return False
		elif city_letter not in [chr(i).upper() for i in range(97, 123)]: 
			return False
		else:
			return True

	def check_identy_number(self, id_num):
		if self.__isValid(id_num):
			city_letter = id_num[0:1]
			city_num = list(str(x[1]) for x in self.code_rule if city_letter in x)[0]
			nums = [int(x) for x in id_num[1:]]
			total_num =  (int(city_num[0:1])*1 + int(city_num[1:])*9 +
			 nums[0]*8 + nums[1]*7 + nums[2]*6 + nums[3]*5 +
			 nums[4]*4 + nums[5]*3 + nums[6]*2 + nums[7]*1 + nums[8]*1)
			if total_num % 10 == 0:
				return True
			else:
				return False
		else:
			return False

		#get city name (ex: 高雄市)
	def get_city(self, id_num):
		city_letter = id_num[0:1]
		city_name = list(str(x[2]) for x in self.code_rule if city_letter in x)[0]
		return city_name

if __name__ == '__main__':
	a = IdentyNumber()
	print(a.get_rules())
	print(a.check_identy_number('G245983256'))
	print(a.get_city('G245983256'))
