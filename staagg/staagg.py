'''staagg: Python library to retrieve commission data from Stagg Web service
'''

__version__ = '1.0'
__author__ = 'Siddharth Saha (sidchilling@gmail.com)'

import xml.etree.ElementTree as ET
import requests

class Staagg(object):
    
    BASE_URL = 'http://www.staagg.com/webservices/v4'

    key = ''
    start_date = None # The start date from which commission data is required
    end_date = None # The end date from which commission data is required
    

    def __init__(self, key, start_date, end_date):
	assert key and start_date and end_date, 'missing args'
	self.key = key
	self.start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S')
	self.end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S')

    def _get_networks(self):
	# This function gets all the networks that have been configured
	url = '%s/getNetworkAccounts/userWsKey/%s' %(self.BASE_URL, self.key)
	r = requests.get(url = url)
	if r.ok:
	    tree = ET.fromstring(r.content)
	    res = [] # Return list - [{'tag' : 'GAN', 'id' : <id>}]
	    networks = tree.find('items').findall('item')
	    for network in networks:
		res.append({
		    'tag' : network.get('tag'), 
		    'id' : network.get('id')})
	    return res
	else:
	    raise Exception('Cannot connect to URL')

    def _get_page_data(self, page_num, network_id):
	url = '%s/getTransactions/userWsKey/%s/startDateTime/%s/endDateTime/%s/dateType/transactionDate/networkAccId/%s/page/%s' \
		%(self.BASE_URL, self.key, self.start_date, self.end_date, network_id, page_num)
	r = requests.get(url = url)
	if r.ok:
	    tree = ET.fromstring(r.content)
	    data = {
		    'page' : int(tree.find('metadata').get('page')),
		    'total_pages' : int(tree.find('metadata').get('totalPages'))
		   }
	    items = tree.find('items').findall('item')
	    commission_data = {}
	    for item in items:
		advertiser_id = item.get('advertiserId') 
		commission_amount = int(item.get('commissionAmount'))
		advertiser_name = item.get('advertiserName')
		if advertiser_id in commission_data:
		    commission_data[advertiser_id]['commission-amount'] = commission_data.get(advertiser_id).get('commission-amount') + \
			    commission_amount
		else:
		    commission_data[advertiser_id] = {
			    'commission-amount' : commission_amount,
			    'advertiser-name' : advertiser_name
			    }
	    data['commission_data'] = commission_data
	    return data
	else:
	    raise Exception('Cannot connect to URL')

    def _get_network_commission_data(self, network):
	# This function will get the commission data for a particular network that has been passed
	res = {} # Of the format {<advertiser-id> : <comission-amount>}
	# We have get the data for all the pages
	page_num = 0 # The page num whose data is to be retrieved
	total_pages = 10
	while page_num < total_pages:
	    data = self._get_page_data(page_num = page_num + 1, network_id = network.get('id'))
	    page_num = data.get('page')
	    total_pages = data.get('total_pages')
	    for advertiser_id in data.get('commission_data').keys():
		if advertiser_id in res:
		    res[advertiser_id]['commission-amount'] = res.get(advertiser_id).get('commission-amount') + \
			    data.get('commission_data').get(advertiser_id).get('commission-amount')
		else:
		    res[advertiser_id] = data.get('commission_data').get(advertiser_id)
	return res

    def get(self):
	'''This method is to be called to get the commission data. The data will be returned
	in the following format -
	{
	    '<advertiser-id>' : {
		    'commission-amount': <amount-in-cents>,
		    'type' : <type-of-network>, (e.g. Commission Junction, Google Affiliate Network etc)
		    'advertiser-name' : <advertiser-name>
		}
	}
	'''
	res = {}
	networks = self._get_networks()
	for network in networks:
	    # Get data for all the networks one-by-one and then aggregate into res
	    commission_data = self._get_network_commission_data(network = network)
	    for advertiser_id in commission_data.keys():
		res[advertiser_id] = {
			'commission-amount' : commission_data.get(advertiser_id).get('commission-amount'),
			'advertiser-name' : commission_data.get(advertiser_id).get('advertiser-name'),
			'type' : network.get('tag')
			}
	return res
