#======LIBRARIES====================================================================
from typing import Dict, List
import json 
import os


#=====VARAIBLES=====================================================================

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct relative paths to your JSON files
special_offers_path = os.path.join(script_dir, "config", "special_offers.json")
items_path = os.path.join(script_dir, "config", "items.json")

with open(special_offers_path) as json_file:
    specialOffersDict = json.loads(json_file.read())

with open(items_path) as json_file:
    itemDict = json.loads(json_file.read())



#====FUNCTIONS====================================================================


def priceFormatter(price)-> str:

    """
    Price formatting function to provide values in pence and pounds.
    """

    if price >= 1:
        return f'£{price:.2f}'
    elif price < 1 and price >0:
        return f'{(price*100):.0f}p'
    else:
        return '0p'

def flatDiscountTotal(item_dict, discount, item, item_count) -> float:
    """
    Calculates the total discount price of a flat discount.
    """
    price = item_dict.get(item, 0)  # Get the price or default to 0 if not found
    discount_price = (price * discount) * item_count
    return round(discount_price, 2)


def calculateTotal(items, itemDict) -> Dict[float,str]:
    """
    Function to calculate the total of a list of items given a dictionary of prices for each item.
    """
    item_prices = [itemDict.get(price, 0) for price in items]  # Get the price or default to 0 if not found
    total = sum(item_prices)
    formatted_total = priceFormatter(total)
    return {"total": (total, f'Basket total: {formatted_total}')}


def flatDiscountFunction(items: List, specialOffersDict: Dict, itemDict: Dict) -> List:
    """"
    Parses through special offer dict and provides special offer prices and message.
    """
    message_list = []
    flat_discount_items = specialOffersDict["offers"]["flat_discount"]["items"]
    for discount_item in flat_discount_items:
        if discount_item[0] in items:
            discount_item_name = discount_item[0]
            discount_item_rate = discount_item[1]
            discount_item_count = items.count(discount_item_name)
            discount = flatDiscountTotal(itemDict, discount_item_rate, discount_item_name, discount_item_count)
            formatted_discount = priceFormatter(discount)
            message_string = f'{discount_item_name.title()} {float(discount_item_rate * 100):.0f}% off: {formatted_discount}'
            message_tuple = (discount, message_string)
            message_list.append(message_tuple)
    return message_list


def buyOneGetOneCheck(items: List, purch_item: str, disc_item: str, purch_item_num: int, disc_item_num: int) -> bool:
    """
    Base logic needs to check whether two items are in the list.
    """
    purch_item_count = items.count(purch_item) // purch_item_num
    disc_item_count = items.count(disc_item) // disc_item_num
    return purch_item_count and disc_item_count > 0


def buyOneGetOneCalc(items: List, disc_item: str, purch_item: str, purch_item_num: int, disc_item_num: int,
                     discount: float, itemDict: Dict) -> float:
    """
    Calculate the total discount from a buy one get one offer.
    """
    disc_item_count = items.count(disc_item) // disc_item_num #count number of feasible item discounts
    purch_item_count = items.count(purch_item) // purch_item_num 
    discount_applicator = purch_item_count
    total_discount = 0
    for _ in range(0, disc_item_count):
        if discount_applicator != 0:
            total_discount += itemDict.get(disc_item, 0) * discount  # Get the price or default to 0 if not found
            discount_applicator += -1
    return total_discount


def bogoDiscountFunction(items: List, specialOffers: Dict, itemDict: Dict) -> List:
    """
    Function for calculating the discount total of a Buy X Get Y discounted value.
    """
    bogo_items = specialOffers['offers']['bogo_discount']['items']
    message_list = []
    #loop through buy one get one (bogo) items and 
    for discount_items in bogo_items:
        purch_item = discount_items[0]
        discount_item = discount_items[1]
        discount_rate = discount_items[2]
        purch_item_num_req = discount_items[3]
        discount_item_num_req = discount_items[4]
        if buyOneGetOneCheck(items, purch_item, discount_item, purch_item_num_req, discount_item_num_req):
            discount = buyOneGetOneCalc(items, discount_item, purch_item, purch_item_num_req, discount_item_num_req,
                                         discount_rate, itemDict)
            discount_formatted = priceFormatter(discount)
            message_string = f'Buy {purch_item_num_req} {purch_item.title()} get {(discount_rate * 100):.0f}% off {discount_item}: {discount_formatted} '
            message_list.append((discount, message_string))
    return message_list


def specialOffersCalc(items: List, itemDict: Dict, specialOffersDict: Dict) -> Dict:
    """
    Needs to return price and string
    """
    offers_list = list(specialOffersDict['offers'].keys())
    message_dict = {}
    if "flat_discount" in offers_list:
        flat_message = flatDiscountFunction(items, specialOffersDict, itemDict)
        message_dict['flat_discount'] = flat_message
    if "bogo_discount" in offers_list:
        bogo_message = bogoDiscountFunction(items, specialOffersDict, itemDict)
        message_dict['bogo_discount'] = bogo_message
    return message_dict


def specialOffersTotal(special_offers_message: Dict) -> float:
    """
    Function that sums the total discount from a special offers message
    """
    offers = special_offers_message.keys()
    total = 0
    for offer in offers:
        total += sum([i[0] for i in special_offers_message[offer]])
    return total


def compileSpecialOfferMessage(special_offer_message_dict: Dict) -> str:
    """
    Function to compile the special offer strings together.
    """
    return ''.join('\n'.join(item[1] for item in value) for value in special_offer_message_dict.values())

#====MAIN========================================================================


def main():
    """
    Main function that outputs:
        Basket price:
        Special offers discount:
        Subtotal (after discount applied):
    """

    items = input("Enter shopping items separated by spaces: ").split()

    specialOffersMessage = specialOffersCalc(items, itemDict, specialOffersDict)
    basketTotalMessage = calculateTotal(items, itemDict)
    specialOffersTotalVal = specialOffersTotal(specialOffersMessage)
    subtotal = basketTotalMessage['total'][0] - specialOffersTotalVal
    subtotal_formatted = priceFormatter(subtotal)
    subtotalMessage = f'Subtotal: {subtotal_formatted}'
    finalBasketMessage = basketTotalMessage['total'][1]
    finalSpecialOfferMessage = compileSpecialOfferMessage(specialOffersMessage)
    if finalSpecialOfferMessage != '':
        final_output = (f"""{finalBasketMessage}
{finalSpecialOfferMessage}
{subtotalMessage}""")
    else:
        final_output = (f"""{finalBasketMessage}
{subtotalMessage}""")

    print(final_output)


if __name__ == '__main__':
    main()







