import requests
import json

def get_cur_curs(curr):
	url='http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
	response = requests.get(url).json()
	for i in response:
		if i['Cur_Abbreviation']==curr:
			return i#['Cur_OfficialRate']
def cur_to_str(cur):
	s = 'За {} {} {} BYN'.format(cur['Cur_Scale'],cur['Cur_Name'],cur['Cur_OfficialRate'])
	return s

def get_all_curr_names():
	url='http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
	response = requests.get(url).json()
	all_curr_names=[]
	for i in response:
		all_curr_names.append(i['Cur_Abbreviation'])
	return all_curr_names

def get_all_curr():
	url='http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
	response = requests.get(url).json()
	return response

def main():
	#print(get_all_curr_names())
	#get_Curr_curs('USD')
	#get_Curr_curs('EUR')
	#print(cur_to_str(get_cur_curs('PLN')))#['Cur_OfficialRate'])
	for i in get_all_curr():
		print(cur_to_str(i))

if __name__ == '__main__':
	main()