# fono - Find Optimal Number of Orders

Pyomo python program to find number of optimal order from websites including shipping costs (MILP)

![](https://raw.githubusercontent.com/kdheepak89/fono/master/screenshot1.png)

## Install

    pip install fono
    pip install fono --upgrade

### Dependencies

* Install [`glpk`](https://www.gnu.org/software/glpk/)

        brew install glpk # osx

## Run

* Run the following to find the optimal order using input in a folder

        fono --folder fono/data

OR

* Run the following to find the optimal order using input from individual files

        fono --quantity fono/data/quantity.csv --price fono/data/price.csv --shipping fono/data/shipping.csv

* Use help

        fono --help

Three files are required to find the optimal order

* prices.csv
* quantity.csv
* shipping.csv

Prices contains the price of an item when purchased from a website.

Quantity contains the number of items required.

Shipping contains the shipping cost from the individual websites.

## Troubleshooting

* Names of items in quantity.csv has to match prices.csv
* Names of websites in shipping.csv has to match prices.csv
* Remove all empty lines

## Contribution

Feel free to submit a pull request.
Thanks to Matt for the inspiration.
