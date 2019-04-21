import requests
import json
from Curr_rates import get_cur_curs,cur_to_str,get_all_curr
from time import sleep,ctime,time 
from bot_opt import token,father_id
#from pogoda import forecast,weather_now
#import random

URL = 'https://api.telegram.org/bot'+token+'/'
Currency = ['AUD', 'BGN', 'UAH', 'DKK', 'USD', 'EUR', 'PLN', 'IRR', 'ISK', 'JPY', 'CAD', 'CNY', 'KWD', 'MDL','NZD', 'NOK', 'RUB', 'XDR', 'SGD', 'KGS', 'KZT', 'TRY', 'GBP', 'CZK', 'SEK', 'CHF']
#command_list=['help','stop','cur','time','aud', 'bgn', 'uah', 'dkk', 'usd', 'eur', 'pln', 'irr', 'isk', 'jpy', 'cad', 'cny', 'kwd', 'mdl',   'nzd', 'nok', 'rub', 'xdr', 'sgd', 'kgs', 'kzt', 'try', 'gbp', 'czk', 'sek', 'chf','basic_curr','forecast']

help_text='Пока этот бот может давать только курсы валют на текущую дату: например /usd и /eur \nПолный перечень валют /cur'
global last_upd
last_upd=0
NewCommands=['help','stop','cur','time','aud', 'bgn', 'uah', 'dkk', 'usd', 'eur', 'pln', 'irr', 'isk', 'jpy', 'cad', 'cny', 'kwd', 'mdl',   'nzd', 'nok', 'rub', 'xdr', 'sgd', 'kgs', 'kzt', 'try', 'gbp', 'czk', 'sek', 'chf','basic_curr','forecast']


def get_updates():
	url = URL + 'getUpdates'
	r = requests.get(url)

	return r.json()
def get_message():
	"""Last message: chat_id and text"""
	data = get_updates()
	try:
		last_obj = data['result'][-1]
		chat_id = last_obj['message']['chat']['id']
		message_text = last_obj['message']['text']
		message_date = last_obj['message']['date']
		message = {'chat_id':chat_id,'text': message_text,'date':message_date}
		return message
	except Exception as e:
		print(type(e))
		return None
	
def send_message(chat_id,text):
	"""Send text-message to chat_id"""
	url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id,text)
	requests.get(url)

def save_all_answers_to_json():
	data = get_updates()	
	with open('updates.json','w') as file:	# save in file
		json.dump(data,file,indent=2,ensure_ascii=False)

def All_Currency():return 'Currency Commands: /'+', /'.join(Currency)

def dec(chat_id,func_name):
	print('in dec')
	def help():send_message(chat_id,help_text)
	def stop():pass
	def time():send_message(chat_id,ctime()) 
	def cur():send_message(chat_id,All_Currency()) 
	def cur_today(curr):return cur_to_str(get_cur_curs(curr))

	f_command=[help,stop,time,cur]
	for i in f_command:
		if func_name.lower()==i.__name__:
			return i()
	if func_name.upper() in Currency:
		send_message(chat_id,cur_today(func_name.upper()))


def main():

	TIME_START=time()
	#react_time=0
	print('start while')
	while True:
		#print('while')
		data = get_updates()
		if data!=None:
			try:
				last_obj = data['result'][-1]
			except Exception as e:
				print(type(e))
				continue
			if TIME_START<last_obj['message']['date']:# we have a message after start
				#print('after start')
				update_id = last_obj['update_id']
				chat_id = last_obj['message']['chat']['id']
				text = last_obj['message']['text']		
				global last_upd
				if last_upd !=update_id: #It is a new message
					last_upd=update_id
					print('text: '+text)
					if '/' in text:
						command=text[1:]
						print('command: '+command)
						if command.lower() in NewCommands:
							print('newcommand')
							dec(chat_id,command)
							
					else: send_message(chat_id,text+'?')
						
			else: pass
		sleep(5)

if __name__ == '__main__':#
	main()