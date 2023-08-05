# fono - Find Optimal Number of Orders

Pyomo python program to find number of optimal order from websites including shipping costs (MILP)

## Dependencies

* Install [`glpk`](https://www.gnu.org/software/glpk/)

        brew install glpk # osx

* [Anaconda 2.7](https://www.continuum.io/downloads)

Clone this repository

* Open a terminal
* Change directory to where you would like to clone this repository

#### Environment

The below will create a python environment called `fono-env`.
If you want a different environment name, open `environment.yml` and change the first line

Open a terminal and run the following

    cd ~/GitRepos/fono # Or change directory to the root of the folder
    conda env create -f environment.yml

## Run

#### Activate the environment

* Open a terminal, and change directory to the root of the folder
* Run the following to activate an environment

        source activate fono-env

* Run the following to find the optimal order using input in a folder

        python fono/run.py --folder fono/data

OR

* Run the following to find the optimal order using input from individual files

        python fono/run.py --quantity fono/data/quantity.csv --price fono/data/price.csv --shipping fono/data/shipping.csv


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
Thanks for Matt for the inspiration.
