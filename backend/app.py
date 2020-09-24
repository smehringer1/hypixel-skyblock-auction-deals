from flask import Flask, request
from bson.json_util import dumps
from query import find_deals, find_item_name, find_lowest_price

app = Flask(__name__)


@app.route('/api')
def home():
    return 'API'

@app.route('/api/auctions')
def get_auctions():
    item_name_underscore = request.args.get('item_name', default = '', type = str)
    if not item_name_underscore.isspace():
        item_name = item_name_underscore.replace("_"," ")
        results = dumps(find_item_name(item_name, True))
        return results

@app.route('/api/auctions/lowest')
def get_lowest_auctions():
    item_name_underscore = request.args.get('item_name', default = '', type = str)
    if not item_name_underscore.isspace():
        item_name = item_name_underscore.replace("_"," ")
        results = dumps(find_lowest_price(item_name, True))
        return results

@app.route('/api/auctions/deals')
def get_deals():
    percentage = request.args.get('percent', type = float)
    minimum_price = request.args.get('minprice', type = int)
    deals = dumps(find_deals(percentage,minimum_price))
    return deals


if __name__ == "__main__":
    app.run()