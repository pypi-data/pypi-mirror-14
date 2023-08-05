from pyomo.environ import *
import ReferenceModel

def solve(instance, solver='glpk', mipgap=0.01):
    solver = SolverFactory(solver)
    solver.options['mipgap'] = mipgap
    instance.preprocess()
    _results = solver.solve(instance, suffixes=['dual'])
    instance.solutions.store_to(_results)
    return(_results)

def display(_results):
    for i in _results['Solution']:
        print("Objective value = {}".format(i['Objective']['Objective']['Value']))

    solution = _results['Solution'][0]
    for item in sorted(solution['Variable'].iteritems()):
        print("{}: {}".format(item[0], item[1]['Value']))


if __name__ == '__main__':

    from data import price, quantity, shipping

    model = ReferenceModel.create_model(price, quantity, shipping)

    display(solve(model))
