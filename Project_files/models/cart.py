from logging import exception


class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, product_id, price, quantity):
        product_id = str(product_id)

        if quantity < 1:
            quantity = 1

        if product_id in self.items:
            print('ahahhha')
            self.items[product_id]['quantity'] += quantity
            self.items[product_id]['price_at_time_of_order'] = price
        else:
            self.items[product_id] = {
                'price_at_time_of_order': price,
                'quantity': quantity,
            }

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
        else:
            raise exception("Product not in cart.")

    def get_total(self):
        return sum([details['price_at_time_of_order'] * details['quantity'] for details in self.items.values()])

    def clear_cart(self):
        self.items = {}

    def get_product_quantity(self, product_id):
        if product_id in self.items:
            return self.items[product_id]['quantity']
        else:
            return 0

    def update_quantity(self, product_id, quantity):

        if quantity < 1:
            quantity = 1

        if product_id in self.items:
            self.items[product_id]['quantity'] = quantity
        else:
            print("Product not in cart.")

    def to_dict(self):
        return self.items

    @staticmethod
    def from_dict(dict):
        cart = Cart()

        cart.items = {str(k): v for k, v in dict.items()}
        cart.items = dict
        return cart

    def __str__(self):
        return str(self.items)

