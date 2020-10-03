import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

connection = pymongo.MongoClient(os.getenv('MONGO'))
db = connection['auctionDB']
auctionDB = db['auctions']
lowestPricesDB = db['lowest_prices']