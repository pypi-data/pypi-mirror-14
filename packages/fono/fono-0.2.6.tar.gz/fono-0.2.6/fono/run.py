#!/usr/bin/env python

import click

import solve
import data
import ReferenceModel
import version

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--folder', type=click.Path(), help='Path to data folder')
@click.option('--quantity', type=click.Path(), help='Path to quantity.csv file')
@click.option('--price', type=click.Path(), help='Path to price.csv file')
@click.option('--shipping', type=click.Path(), help='Path to shipping.csv file')
@click.option('--color', hidden=True, default='white', help='Color of solution (e.g. --color=red)')
@click.option('--fono_color', hidden=True, default='green', help='Color of solution (e.g. --fono_color=blue)')
@click.version_option(version.__version__, '-v', '--version')
def main(**kwargs):
    """
    'Find Optimal Number of Orders' aka fono
    """
    color = kwargs.pop('color')
    fono_color = kwargs.pop('fono_color')

    try:
        if not any([kwargs[key] for key in kwargs]):
            help_str = "{}".format(click.get_current_context().get_help())
            click.secho(help_str)
            click.get_current_context().exit()

        def show_item(item):
            if item is not None:
                return(item)

        click.echo("")
        click.secho("Find the Optimal Number of Orders:", fg=fono_color, bold=True)
        click.echo("")

        with click.progressbar(('Getting data', 'Creating model', 'Solving', 'Finished'), label='fono:', item_show_func=show_item) as bar:
            for item in bar:
                if item == 'Getting data':
                    if kwargs['folder']:
                        price, quantity, shipping = data.get_input(kwargs['folder'])
                    elif kwargs['quantity'] and kwargs['price'] and kwargs['shipping']:
                        quantity = data.get_quantity(kwargs['quantity'])
                        price = data.get_price(kwargs['price'])
                        shipping = data.get_shipping(kwargs['shipping'])
                elif item == 'Creating model':
                    model = ReferenceModel.create_model(price, quantity, shipping)
                elif item == 'Solving':
                    solve.solve_instance(model), model

        # solve.display_results(solve.solve_instance(model), model)

        click.echo("")

        click.secho("fono results:", fg=fono_color, bold=True)

        click.echo("")

        for item in sorted(model.Items):
            for website in sorted(model.Websites):
                if model.Quantity[website, item].value>0:
                    click.echo("Buy ", nl=False)
                    click.secho("{} ".format(int(model.Quantity[website, item].value)),
                            fg=color, bold=True, nl=False)
                    click.echo("item(s) of ", nl=False)
                    click.secho("{} ".format(item),
                            fg=color, bold=True, nl=False)
                    click.echo("from ", nl=False)
                    click.secho("{} ".format(website),
                            fg=color, bold=True, nl=False)
                    click.echo("for a total of ", nl=False)
                    click.secho("{} ".format(price[(website, item)] * model.Quantity[website, item].value),
                            fg=color, bold=True, nl=False)
                    click.echo("dollars", nl=False)
                    click.secho(".".format(website))


        click.echo("")

        item_costs = model.Cost['Item'].value
        shipping_costs = model.Cost['Shipping'].value
        total_costs = item_costs + shipping_costs

        click.secho("Total product costs = {}".format(item_costs), bold=True)
        click.secho("Total shipping costs = {}".format(shipping_costs), bold=True)
        click.echo("")
        click.secho("Total costs = {}".format(total_costs), fg=fono_color, bold=True)
        click.echo("")

    except Exception as e:
        click.echo('')
        raise click.ClickException("{}\n\nCheck the help (--help) on how to use fono or contact the developer.".format(e.message))

if __name__ == '__main__':
    main()
