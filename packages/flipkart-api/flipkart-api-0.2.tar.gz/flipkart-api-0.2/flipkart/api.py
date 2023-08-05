import requests
import json,pdb

class FlipkartApi(object):
	def __init__(self, Fk_Affiliate_Id, Fk_Affiliate_Token, **kwargs):
		self.Fk_Affiliate_Token = Fk_Affiliate_Token
		self.Fk_Affiliate_Id = Fk_Affiliate_Id

	def lookup(self, **kwargs):
		data = {'id': kwargs['id'] }
		header = {
            'Fk-Affiliate-Token':self.Fk_Affiliate_Token ,
            'Fk-Affiliate-Id':self.Fk_Affiliate_Id,
            }

		r = requests.get('https://affiliate-api.flipkart.net/affiliate/product/json',params = data ,headers=header)
		data = json.loads(r._content)
		return Product(data)

class Product(object):
	def __init__(self, data):
		self.data = data

	@property
	def title(self):
		title = self.data['productBaseInfo']['productAttributes']['title']
		return title
	
	@property
	def sp(self):
		sp = self.data['productBaseInfo']['productAttributes']['sellingPrice']
		return sp

	@property
	def url(self):
		url = self.data['productBaseInfo']['productAttributes']['productUrl']
		return url
	