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
    try:
        my_want = CarousellSearch(search_query[0], results=config.RESULTS_COUNT)
        results = my_want.send_request()

        count = 0
        line_item = ""
        for item in results:
            r = item['listingCard']
            count += 1
            print("{}) {}".format(str(count), r))
            # skip results without query in listing title OR description
            want = search_query[0].lower()
            itemTitle = r['title']
            itemPrice = float(r['price'].lstrip("S$"))
            minPrice = search_query[1]
            maxPrice = search_query[2]
            sellerUserName = r['seller']['username']
            targetPrice = search_query[3]
            itemImage = r['photoUrls'][0]
            itemLikes = r['likesCount']
            itemLink = "https://sg.carousell.com/p/" + re.sub('[^A-Za-z0-9\-]+', '', itemTitle.lower().replace(" ", "-")) + "-" + str(r['id'])


            # if want not in (itemTitle).lower() and want not in (r['description']).lower():
            #     print("Out of search. Skip! " + (itemTitle))
            #     continue

            # # Check if item is within specified price range
            # if itemPrice <= minPrice or itemPrice >= maxPrice:
            #     print("Price out of range. Ignore!")
            #     continue

            # # Ignore items with unwanted keywords
            # if any([ign in itemTitle.lower() for ign in config.IGNORES_IN_TITLE]) or any(
            #         [ign in r['description'].lower() for ign in config.IGNORES]):
            #     print("Item ignored!")
            #     continue

            # check if listing is in DB already
            check = (session.query(CarousellListing).filter_by(listing_id=r['id']).
                     first())

            postedTime = arrow.get(r['aboveFold'][0]['timestampContent']['seconds']['low']).format('DD/MM/YYYY HH:MM')

            # Details of item
            item_details = itemLink + "\n" +\
                        sellerUserName + "(https://sg.carousell.com/" + sellerUserName + ")\n" + \
                         itemTitle + "\n" +\
                         ":heavy_dollar_sign:" + str(itemPrice) + "\n" + \
                         helpers.multiplyEmoji(":heart:", int(itemLikes)) + "\n" + \
                         postedTime + "\n"

            # if it is not in DB
            if check is None:
                line_item = item_details

                # Add highlight when target price is met
                # if itemPrice <= targetPrice:
                #     line_item += helpers.multiplyEmoji(":heavy_dollar_sign:", 8)

                line_item += "\n\n"

                helpers.postMessage(line_item, itemImage)

                listing = CarousellListing(
                    listing_id=r['id'],
                    seller=sellerUserName,
                    title=itemTitle,
                    currency_symbol="S$",
                    price=itemPrice,
                    time=postedTime,
                    likes=itemLikes,
                )
                session.add(listing)
                session.commit()

            else:
                print("Item checked before!")
                if check is not None:
                    line_item = item_details
                    isChanged = False

                    if itemPrice < float(check.price):
                        line_item += helpers.multiplyEmoji(":exclamation:", 3) + "ITEM PRICE HAS BEEN REDUCED" + \
                                     helpers.multiplyEmoji(":exclamation:", 3) + "\n Old price::heavy_dollar_sign:" + '%.2f' % check.price
                        line_item += "\n\n"
                        check.price = itemPrice
                        isChanged = True

                    if itemTitle != check.title:
                        line_item += helpers.multiplyEmoji(":grey_exclamation:", 3) + "ITEM TITLE HAS CHANGED" + \
                                     helpers.multiplyEmoji(":grey_exclamation:",
                                                           3) + "\n Old title: " + check.title
                        line_item += "\n\n"
                        check.title = itemTitle
                        isChanged = True

                    if check.likes == None:
                        check.likes = 0

                    if int(itemLikes) >= check.likes + config.LIMIT_1:
                        line_item += helpers.multiplyEmoji(":heartpulse:", 3) + "ITEM :heart: HAS CHANGED" + \
                                     helpers.multiplyEmoji(":heartpulse:",
                                                           3) + "\n Old : " + str(check.likes) + ":heart:"
                        line_item += "\n\n"
                        check.likes = itemLikes
                        isChanged = True

                    if isChanged:
                        helpers.postMessage(line_item)

                    session.commit()

        return
    except Exception as e:
        type, fname, lineno = helpers.getFormattedException()
        message = helpers.multiplyEmoji(":x:", 3) + "ERROR: {} \n{} {} {}".format(e, type, fname, lineno)
        print(message)
        helpers.postMessage(message)
