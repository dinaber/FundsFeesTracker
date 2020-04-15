"""
Created by @Dina
Jan 2020
"""

from urllib.request import urlopen, Request
from pushbullet import PushBullet
import re
import pandas as pd
import os
import warnings
import argparse
from datetime import date

def main(output_mode, test_mode, funds_info_file, output_file, pushbullet_key): 
	funds_info = pd.read_csv(os.path.join(os.getcwd(), funds_info_file), float_precision='high')
	nfunds = len(funds_info['fund number'])   
	
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,} 
	url_base = "https://www.funder.co.il/fund/"
	messages = []
	for inx in range(nfunds):
		fund_number = funds_info['fund number'][inx]
		request = Request(url_base+str(fund_number), None, headers) #The assembled request
		response = urlopen(request)
		# page source: 
		data = response.read() # The data u need
		nihol = re.findall(r'"nihol":(.*?),', data.decode('utf-8'))
		nemanut = re.findall(r'"nemanut":(.*?),', data.decode('utf-8'))
		if len(nihol)>1 or len(nihol)==0:
			msg = f'More than 1 value or no values for nihol for fund {str(fund_number)} was found, skipping fund'
			messages.append(msg)
			warnings.warn(msg)
			continue
		if len(nemanut)>1 or len(nemanut)==0:
			msg = f'More than 1 value or no values for nemanut for fund {str(fund_number)} was found, skipping fund'
			messages.append(msg)
			warnings.warn(msg)
			continue

		nihol = round(float(nihol[0]),3)
		nemanut = round(float(nemanut[0]),3)

		# compare with current value:
		if nihol!=funds_info['nihol (%)'][inx]:
			msg = f"For fund number {str(fund_number)} the nihol fee changed! It was {funds_info['nihol (%)'][inx]} and now {nihol}"
			messages.append(msg)
		if nemanut!=funds_info['nemanut (%)'][inx]:
			msg = f"For fund number {str(fund_number)} the nemanut fee changed! It was {funds_info['nemanut (%)'][inx]} and now {nemanut}"
			messages.append(msg)

	if test_mode=='on' or len(messages)>0:		   
		if test_mode=='on':
			title = "test"
			text = 'This is a test'
		else:
			title = "Funds update"
			messages.append('#########')
			messages.append('Note:') 
			messages.append('* If any of your fees changed, update them in the csv to avoid getting repeated messages')
			messages.append('* If you recieved a warning regarding one of the funds maybe something is FISHY. Either correct it or remove it from the list')
			text = '\n'.join(messages)
		if output_mode=='push' or output_mode=='both':
			pb = PushBullet(pushbullet_key)
			push = pb.push_note(title,text)
		if output_mode=='file' or output_mode=='both':
			with open(output_file, "a") as f:
				today = date.today()
				f.write(f"Date: {today}\n")
				f.write(text)
				f.write(f'\n\n')



if __name__=="__main__":
	# Define the parser
	parser = argparse.ArgumentParser(description='Funds fee tracker app')
	parser.add_argument('--mode', action="store", dest='output_mode', default='file', choices=['file', 'push', 'both'], help='Choose your output form, "file" (default) to write to file or "push" for pushbullet')
	parser.add_argument('--test', action="store", dest='test_mode', default='off', choices=['on', 'off'], help='Run in test mode to check that it works')
	parser.add_argument('--p_key', action="store", dest='pushbullet_key', default=None, help='Your pushbullet key (optional). Only if mode is push')
	parser.add_argument('--funds', action="store", dest='funds_info_file', default='funds_fees.csv', help='Full path to funds csv file. default: funds_fees.csv (searches in current directory)')
	parser.add_argument('--o', action="store", dest='output_file', default='output.txt', help='Full path to output file (optional). Only if mode is "file"')
	# Now, parse the command line arguments and store the values in the `args` variable
	args = parser.parse_args()
	main(args.output_mode, args.test_mode, args.funds_info_file,args.output_file, args.pushbullet_key)
