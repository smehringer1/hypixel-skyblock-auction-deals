import pymongo
import json
import requests
import time
import statistics
import os
from dotenv import load_dotenv
load_dotenv()


connection = pymongo.MongoClient(os.getenv('MONGO_DOCKER'))
db = connection['db']
auctionDB = db['auctions']
lowestPricesDB = db['lowest_prices']

API_BASE = 'https://api.hypixel.net/skyblock/auctions?page='
KEY = os.getenv('API_KEY')

weapon_reforges = ('Gentle','Odd','Fast','Fair','Epic','Sharp','Heroic','Spicy','Legendary','Deadly','Fine','Grand','Hasty','Neat','Rapid','Unreal','Awkward','Rich','Fabled','Suspicious','Gilded','Precise')
armor_reforges = ('Clean','Fierce','Heavy','Light','Mythic','Pure','Smart','Titanic','Wise','Very','Highly','Extremely','Not So','Absolutely','Perfect','Necrotic','Spiked','Renowned','Cubic','Warped','Reinforced','Loving','Ridiculous')
fishingrod_reforges = ('Salty', 'Treacherous')
accessory_reforges = ('Bizarre','Itchy','Ominous','Pleasant','Pretty','Shiny','Simple','Strange','Vivid','Godly','Demonic','Forceful','Hurtful','Keen','Strong','Superior','Unpleasant','Zealous','Silky','Bloody')
tool_reforges = ('Fruitful','Magnetic')

reforges = weapon_reforges + armor_reforges + accessory_reforges + fishingrod_reforges + tool_reforges
checked_names = ('Wise Dragon','Strong Dragon','Superior Dragon','Perfect Helmet','Perfect Chestplate','Perfect Leggings','Perfect Boots','Heavy Helmet','Heavy Chestplate','Heavy Leggings','Heavy Boots')

update_times = []

# def update_auction_page(page,timestamp):
#     start_time_page = time.time()
#     res = requests.get(API_BASE + str(page) + KEY).json()
#     print('Time to fetch: ' + str(time.time()-start_time_page))
#     auctions = res['auctions']
#     start_time_auctions = time.time()
#     for auction in auctions:
#         uuid = auction['uuid']
#         simplified = modify_auction_data(auction)
#         auctionDB.update_one({'uuid' : uuid}, {'$set' : simplified}, upsert = True)
#     update_times.append(time.time()-start_time_auctions)
#     print('Updated page ' + str(res['page']))
#     duration = time.time()-start_time_page
#     print('Duration: ' + str(duration) + '\n')
#     if duration < 0.6:
#         time.sleep(.5)

# def update_all_auctions():
#     print('Update started...')
#     start_time = time.time()
#     res = requests.get(API_BASE + str(0) + KEY).json()
#     total_pages = res["totalPages"]
#     for i in range(0,total_pages):
#         update_auction_page(i,start_time)
#     removed = auctionDB.delete_many({'updated_time' : {'$ne' : start_time}})
#     print('Update took ' + str(time.time() - start_time))
#     print('Average DB query took: ' + str(statistics.mean(update_times)))
#     print(str(removed.deleted_count) + ' documents were removed\n')
#     update_lowest_prices()

def modify_auction_data(auction):
    reforge = ''
    stars = ''
    pet_level = ''
    item_name = auction['item_name']
    if item_name.startswith(reforges):
        if not item_name.startswith(checked_names):
            item_name_split = item_name.split(' ', 1)
            item_name = item_name_split[1]
            reforge = item_name_split[0]
    elif item_name.startswith('['):
        item_name_split = item_name.split(' ', 2)
        item_name = item_name_split[2]
        pet_level = item_name_split[1][:-1]
    if item_name.endswith('✪'):
        item_name_split = item_name.rsplit(' ', 1)
        item_name = item_name_split[0]
        stars = item_name_split[1].count('✪')
    if item_name.startswith('◆'):
        item_name = item_name.split(' ',1)[1]
    auction_modified = {
            'uuid' : auction['uuid'],
            #'start' : auction['start'],
            #'end' : auction['end'],
            'item_name' : item_name,
            'reforge' :  reforge,
            'stars' : stars,
            #'item_lore' : auction['item_lore'],
            'extra' : auction['extra'],
            'category' : auction['category'],
            'pet_level' : pet_level,
            'tier' : auction['tier'],
            'starting_bid' : auction['starting_bid'],
            #'claimed' : auction['claimed'],
            'bin' : auction.get('bin', False),
        }
    return auction_modified



def update_all_auctions():
    print('Update started...')
    #uuid_index = pymongo.IndexModel([('uuid' , pymongo.ASCENDING)],name='uuid')
    item_name_price_index = pymongo.IndexModel([('item_name',pymongo.TEXT),('starting_bid',1)],name='item_name_text_starting_bid')
    update_times = []
    start_time = time.time()
    auctionsDB_new = db['auctions_new']
    auctionsDB_new.create_indexes([item_name_price_index])
    page = 0
    while True:
        start_time_loop = time.time()
        print('Fetching page '  + str(page) + '...')
        res = requests.get(API_BASE + str(page) + KEY).json()
        print("Fetch took: "  + str(time.time() - start_time_loop))
        update_time_start = time.time()
        if res['success']:
            auctions = res['auctions']
            for i in range(0,len(auctions)):
                auctions[i] = modify_auction_data(auctions[i])
            auctionsDB_new.insert_many(auctions,ordered=False)
            update_time = time.time() - update_time_start
            update_times.append(update_time)
            print('Updated page ' + str(page))
            page += 1
        else:
            break
    auctionDB.drop()
    auctionsDB_new.rename('auctions')
    print('Update took ' + str(time.time() - start_time))
    print('Average DB query took: ' + str(statistics.mean(update_times)))
    update_lowest_prices()


def update_lowest_prices():
    print('Updating lowest price list...')
    pipeline = [
        {'$match' : {'bin' : True}},
        {'$group' : {'_id' : '$item_name', 'lowest' : {'$min' : '$starting_bid' }}},
        {'$sort' : {'lowest' : 1}}
        ]
    results = auctionDB.aggregate(pipeline)
    time_stamp = time.time()
    for result in results:
        lowestPricesDB.update_one({'_id' : result['_id']},{'$set' : {'_id' : result['_id'], 'lowest' : result['lowest'], 'timestamp' : time_stamp }}, upsert=True)
    removed = lowestPricesDB.delete_many({'timestamp' : {'$ne' : time_stamp}})
    print('Updated, ' + str(removed.deleted_count) + ' documents were removed')

if __name__ == '__main__':
    update_all_auctions()