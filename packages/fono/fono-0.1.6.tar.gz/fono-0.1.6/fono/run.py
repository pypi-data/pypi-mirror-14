#! /usr/bin/env python

import click

import solve
import data
import ReferenceModel

@click.group()
def cli():
    pass

@cli.command()
@click.option('--folder', type=click.Path())
@click.option('--quantity', type=click.Path())
@click.option('--price', type=click.Path())
@click.option('--shipping', type=click.Path())
def main(**kwargs):
    if kwargs['folder']:
        quantity, price, shipping = data.get_input(kwargs['folder'])
    elif kwargs['quantity'] and kwargs['price'] and kwargs['shipping']:
        quantity = data.get_quantity(kwargs['quantity'])
        price = data.get_price(kwargs['price'])
        shipping = data.get_shipping(kwargs['shipping'])
    else:
        raise click.UsageError("foo requires either a path to a folder or paths to ALL input files. Check the documentation for how to use foo.")

    model = ReferenceModel.create_model(price, quantity, shipping)

    solve.display(solve.solve(model))

if __name__ == '__main__':
    main()
