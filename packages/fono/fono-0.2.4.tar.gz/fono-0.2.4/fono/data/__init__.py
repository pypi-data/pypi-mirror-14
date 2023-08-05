price = {
    ('website1', 'item1'): 1,  # dollars
    ('website2', 'item1'): 2,  # dollars
    ('website1', 'item2'): 1,  # dollars
    ('website2', 'item2'): 2,  # dollars
    ('website1', 'item3'): 1,  # dollars
    ('website2', 'item3'): 2,  # dollars
    ('website1', 'item4'): 1,  # dollars
    ('website2', 'item4'): 2,  # dollars
    ('website1', 'item5'): 1,  # dollars
    ('website2', 'item5'): 2,  # dollars
}

quantity = {
    'item1': 10,  # number of items
    'item2': 0,  # number of items
    'item3': 0,  # number of items
    'item4': 0,  # number of items
    'item5': 0,  # number of items
}

shipping = {
    'website1': 21,
    'website2': 10
}

import os
import csv

def get_input(folder, quantity_file='quantity.csv', price_file='price.csv', shipping_file='shipping.csv'):
    folder_name = (os.path.abspath(folder))

    quantity = get_quantity(os.path.join(folder_name, quantity_file))
    price = get_price(os.path.join(folder_name, price_file))
    shipping = get_shipping(os.path.join(folder_name, shipping_file))

    return price, quantity, shipping

def get_quantity(f):
    quantity = {}
    with open(f, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row[1] = float(row[1])
            if int(row[1]) == row[1]:
                quantity[row[0]] = row[1]
            else:
                raise Exception("Quantity {} must be an integer".format(row[1]))
    return quantity

def get_price(f):
    price = {}

    with open(f, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row[2] = float(row[2])
            price[(row[0], row[1])] = row[2]

    return price

def get_shipping(f):

    shipping = {}

    with open(f, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row[1] = float(row[1])
            shipping[row[0]] = row[1]

    return shipping
