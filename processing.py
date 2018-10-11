import arrow
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import helpers
import myconfigurations as config
from pycarousell import CarousellSearch
import re
Base = declarative_base()

class CarousellListing(Base):
    __tablename__ = 'itemlistings'
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer)
    seller = Column(String)
    title = Column(String)
    currency_symbol = Column(String)
    price = Column(Float)
    time = Column(String)
    likes = Column(Integer)

engine = create_engine('sqlite:///searchListings.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def find_stuff(index, search_query):
    my_want = CarousellSearch(search_query, results=config.RESULTS_COUNT)
    try:
        results = my_want.send_request()
    except Exception as e:
        results = []
        type, fname, lineno = helpers.getFormattedException()
        message = helpers.multiplyEmoji(":x:", 3) + "ERROR IN API REQUEST: {} \n{} {} {}".format(e, type, fname, lineno)
        print(message)
        robot.post_message(message)

    count = 0
    line_item = ""
    for r in results:
        count += 1
        print("{}) {}".format(str(count), r))
        #skip results without query in listing title OR description
        want = search_query.lower()
        itemTitle = r['title']
        itemPrice = float(r['price'])
        minPrice = config.PRICE_MINIMUM[index]
        maxPrice = config.PRICE_MAXIMUM[index]
        sellerUserName = r['seller']['username']
        targetPrice = config.PRICE_TARGET[index]
        itemImage = r['primary_photo_url']
        itemLikes = r['likes_count']

        if want not in (r['title']).lower() and want not in (r['description']).lower():
            print("Out of search. Skip! " + (r['title']))
            continue

        # Check if item is within specified price range
        if itemPrice <= minPrice or itemPrice >= maxPrice:
            print("Price out of range. Ignore!")
            continue

        # Ignore items with unwanted keywords
        if any([ign in r['title'].lower() for ign in config.IGNORES_IN_TITLE]) or any([ign in r['description'].lower() for ign in config.IGNORES]):
            print("Item ignored!")
            continue

        #check if listing is in DB already
        check = (session.query(CarousellListing).filter_by(listing_id=r['id']).
                    first())


        # Details of item
        item_details = "https://sg.carousell.com/p/" + re.sub('[^A-Za-z0-9\-]+', '', itemTitle.lower().replace(" ", "-")) + "-" + str(r['id']) + "\n" +\
                    sellerUserName + "(https://sg.carousell.com/" + sellerUserName + ")\n" + \
                     r['title'] + "\n" +\
                     ":heavy_dollar_sign:" + str(itemPrice) + "\n" + \
                     helpers.multiplyEmoji(":heart:", int(itemLikes)) + "\n" + \
                     arrow.get(r['time_indexed']).format('DD/MM/YYYY HH:MM') + "\n"

        #if it is not in DB
        if check is None:
            line_item = item_details

            # Add highlight when target price is met
            if itemPrice <= targetPrice:
                line_item += helpers.multiplyEmoji(":heavy_dollar_sign:", 8)

            line_item += "\n\n"

            helpers.postMessage(line_item, itemImage)

            listing = CarousellListing(
                listing_id = r['id'],
                seller =sellerUserName,
                title = itemTitle,
                currency_symbol = r['currency_symbol'],
                price = itemPrice,
                time = arrow.get(r['time_created']).format('DD/MM/YYYY HH:MM'),
                likes = itemLikes,
            )
            session.add(listing)
            session.commit()

        else:
            print("Item checked before!")
            if check is not None:
                line_item = item_details

                isChanged=False
                if itemPrice < float(check.price):
                    line_item = item_details
                    line_item += helpers.multiplyEmoji(":exclamation:", 3) + "ITEM PRICE HAS BEEN REDUCED" + \
                                 helpers.multiplyEmoji(":exclamation:", 3) + "\n Old price::heavy_dollar_sign:" + '%.2f' % check.price
                    line_item += "\n\n"
                    check.price = itemPrice
                    isChanged = True

                if itemTitle != check.title:
                    line_item = item_details
                    line_item += helpers.multiplyEmoji(":grey_exclamation:", 3) + "ITEM TITLE HAS CHANGED" + \
                                 helpers.multiplyEmoji(":grey_exclamation:",
                                                       3) + "\n Old title: " + check.title
                    line_item += "\n\n"
                    check.title = itemTitle
                    isChanged = True

                if itemLikes != check.likes:
                    line_item = item_details
                    line_item += helpers.multiplyEmoji(":heartpulse: ", 3) + "ITEM :heart: HAS CHANGED" + \
                                 helpers.multiplyEmoji(":heartpulse: ",
                                                       3) + "\n Old likes: " + str(itemLikes) + ":heart:"
                    line_item += "\n\n"
                    check.likes = itemLikes
                    isChanged = True

                if isChanged:
                    helpers.postMessage(line_item)

                session.commit()

    return
