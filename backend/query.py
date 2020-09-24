from db_updater import lowestPricesDB,auctionDB
import json


def find_item_name(itemName, binEnabled):
    pipeline = [
        {'$match' : {'$text' : {'$search' : "\"{}\"".format(itemName)}, 'bin' : binEnabled}},
        {'$project' : {'_id' : 0, 'uuid' : 0 ,'extra' : 0, 'updated_time' : 0, 'claimed' : 0}},
        {'$sort' : {'starting_bid' : 1}}
    ]
    results = auctionDB.aggregate(pipeline)
    return results

def find_lowest_price(itemName, binEnabled):
    pipeline = [
        {'$match' : {'$text' : {'$search' : "\"{}\"".format(itemName)}, 'bin' : binEnabled}},
        {'$group' : {'_id' : '$item_name', 'lowest' : {'$min' : '$starting_bid' }}},
        {'$sort' : {'lowest' : 1}}
        ]
    results = auctionDB.aggregate(pipeline)
    return results

def find_deals(percent_off_threshold,minimum_price):
    percent_of = 1 - percent_off_threshold
    deals = []
    pipeline = [
        {'$match' : {'bin' :  True}},
        {'$sort' : {'item_name' : 1, 'starting_bid' : 1}},
        {'$group' : {
            '_id' : '$item_name',
            'items' : {'$push' : {'item_name' : '$item_name', 'price' : '$starting_bid'}} 
        }},
        {'$project' : {
            'item' : {'$arrayElemAt' : ['$items' , 1]}
        }},
        {'$project' : {'price' : '$item.price'}},
        {'$sort' : { '_id' : 1 }}
    ]
    results = auctionDB.aggregate(pipeline)
    for result in results:
        item_name = result['_id']
        query = lowestPricesDB.find_one({'_id' : item_name})
        second_lowest_price = result.get('price',0)
        lowest_price = query.get('lowest')
        if not second_lowest_price == 0:
            percent = lowest_price / second_lowest_price
            if second_lowest_price >= minimum_price:
                if lowest_price / second_lowest_price < percent_of:
                    deal = {'item_name' : item_name, 'lowest_price' : lowest_price, 'second_lowest_price' : second_lowest_price, 'percentage' : round(percent, 2)}
                    deals.append(deal)
    return deals