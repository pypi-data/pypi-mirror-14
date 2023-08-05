import requests
import json,pdb

class FlipkartApi(object):
	def __init__(self, Fk_Affiliate_Id, Fk_Affiliate_Token, **kwargs):
		self.Fk_Affiliate_Token = Fk_Affiliate_Token
		self.Fk_Affiliate_Id = Fk_Affiliate_Id

	def lookup(self, **kwargs):
		ids = kwargs['id']
		ids = ids.split(',')
		header = {
				'Fk-Affiliate-Token':self.Fk_Affiliate_Token ,
				'Fk-Affiliate-Id':self.Fk_Affiliate_Id,
				}
		products =[]
		for i in ids:
			data = {'id': i }
			r = requests.get('https://affiliate-api.flipkart.net/affiliate/product/json',params = data ,headers=header)
			data = json.loads(r._content)
			products.append(Product(data))
		if len(products) == 1:
			return products[0]
		else:
			return products

class Product(object):
	def __init__(self, data):
		self.data = data

	@property
	def title(self):
		title = self.data['productBaseInfo']['productAttributes']['title']
		return title
	
	@property
	def selling_price(self):
		sp = self.data['productBaseInfo']['productAttributes']['sellingPrice']
		return sp

	@property
	def url(self):
		url = self.data['productBaseInfo']['productAttributes']['productUrl']
		return url

	@property
	def mrp(self):
		mrp = self.data['productBaseInfo']['productAttributes']['maximumRetailPrice']['amount']
		return self.mrp

	@property
	def description(self):
		des = self.data['productBaseInfo']['productAttributes']['productDescription']
		return self.description
	
	@property
	def cod(self):
		return self.data['productBaseInfo']['productAttributes']['codAvailable']

	@property
	def emi(self):
		return self.data['productBaseInfo']['productAttributes']['emiAvailable']

	@property
	def offers(self):
		return self.data['productBaseInfo']['productAttributes']['offers']

	@property
	def discount_percentage(self):
		return self.data['productBaseInfo']['productAttributes']['discountPercentage']

	@property
	def brand(self):
		return self.data['productBaseInfo']['productAttributes']['productBrand']

	@property
	def instock(self):
		return self.data['productBaseInfo']['productAttributes']['inStock']

	@property
	def images(self):
		return self.data['productBaseInfo']['productAttributes']['imageUrls']

	@property
	def color(self):
		return self.data['productBaseInfo']['productAttributes']['color']

	@property
	def size(self):
		return self.data['productBaseInfo']['productAttributes']['size']

	@property
	def productid(self):
		return self.data['productBaseInfo']['productIdentifier']['productId']
	
	
	

	

	
	
	

	
	
	