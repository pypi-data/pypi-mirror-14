"""
Pyomo
"""
from __future__ import division
from pyomo.environ import *

"""
Example -

    price = {
        ('website1', 'item1'): 1, # dollars
        ('website2', 'item1'): 2, # dollars
        ('website1', 'item2'): 1, # dollars
        ('website2', 'item2'): 2, # dollars
        ('website1', 'item3'): 1, # dollars
        ('website2', 'item3'): 2, # dollars
        ('website1', 'item4'): 1, # dollars
        ('website2', 'item4'): 2, # dollars
        ('website1', 'item5'): 1, # dollars
        ('website2', 'item5'): 2, # dollars
            }

    quantity = {
        'item1': 10, # number of items
        'item2': 0, # number of items
        'item3': 0, # number of items
        'item4': 0, # number of items
        'item5': 0, # number of items
               }

    shipping = {
        'website1': 21,
        'website2': 10
    }
"""

LargeNumber = 99999

def create_model(price, quantity, shipping):

    model = ConcreteModel()

    model.Websites = Set(initialize=set([i[0] for i in price]))
    model.Items = Set(initialize=set([i[1] for i in price]))

    model.Quantity = Var(model.Websites, model.Items, domain=NonNegativeReals)
    model.Purchased = Var(model.Websites, within=Binary)

    model.CostSet = Set(initialize=['Item', 'Shipping'])
    model.Cost = Var(model.CostSet, within=NonNegativeReals)

    def objective_rule(m):
        return sum(m.Cost[i] for i in m.CostSet)

    def item_cost_rule(m):
        return m.Cost['Item'] == sum(price[(w, i)] * m.Quantity[w, i] for w in m.Websites for i in m.Items)

    model.ItemCost = Constraint(rule=item_cost_rule)

    def shipping_cost_rule(m):
        return m.Cost['Shipping'] == sum(shipping[w] * m.Purchased[w] for w in m.Websites)

    model.ShippingItemCost = Constraint(rule=shipping_cost_rule)

    def posbigM_rule(m, w):
        return sum(m.Quantity[w, i] for i in m.Items) - m.Purchased[w] * LargeNumber <= 0

    def negbigM_rule(m, w):
        return sum(m.Quantity[w, i] for i in m.Items) + (1 - m.Purchased[w]) * LargeNumber >= 0

    model.BigMConstraintpos = Constraint(model.Websites, rule=posbigM_rule)
    model.BigMConstraintneg = Constraint(model.Websites, rule=negbigM_rule)

    def quantity_rule(m, i):
        return sum(m.Quantity[w, i] for w in m.Websites) >= quantity[i]

    model.QuantityConstraint = Constraint(model.Items, rule=quantity_rule)

    model.Objective = Objective(rule=objective_rule)

    return model
