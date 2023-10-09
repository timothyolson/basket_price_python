import basket_price_app
import unittest

item_dict = {"apples": 1.00, "soup": 1.50, "bread": 1.40, "milk": 3.00}
special_offers_dict = {
    "offers": {
      "flat_discount": {
        "items": [["apples", 0.10]]
      },
      "bogo_discount": {
        "items": [["soup", "bread", 0.50, 2, 1]]
      }
    }
  }

class BasketPriceAppTest(unittest.TestCase):

    def test_price_formatter(self):
        high_value = basket_price_app.priceFormatter(3.50)
        self.assertEqual(high_value, "£3.50")
        print("priceFormatter(3.50) resulted in {high_value}")
        low_value = basket_price_app.priceFormatter(0.1)
        self.assertEqual(low_value, "10p")
        print("priceFormatter(0.1) resulted in {low_value}")

    def test_flat_discount_function(self):
        items = ["eggs","milk","soup","apples"]
        message = basket_price_app.flatDiscountFunction(items,
                                                        special_offers_dict,
                                                        item_dict)
        self.assertEqual(message,[(0.1,"Apples 10% off: 10p")])
        print(f"flat discount function returned: {message}")


    def test_buy_one_get_one_check(self):
        items = ["eggs","milk","soup","apples","soup","bread"]
        boolean_check = basket_price_app.buyOneGetOneCheck(items,"bread","soup",2,1)
        self.assertEqual(boolean_check,False)



if __name__ == '__main__':
    unittest.main()