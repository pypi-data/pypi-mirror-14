import ReferenceModel

def solve_instance(instance, solver='glpk', mipgap=0.01):
    solver = ReferenceModel.SolverFactory(solver)
    solver.options['mipgap'] = mipgap
    instance.preprocess()
    _results = solver.solve(instance, suffixes=['dual'])
    instance.solutions.store_to(_results)
    return(_results)

def display_results(_results, model):
    print("Optimal solution:\n")
    for website in sorted(model.Websites):
        for item in sorted(model.Items):
            if model.Quantity[website, item].value>0:
                print("Buy {q} item(s) of {i} from {w}".format(q=int(model.Quantity[website, item].value),
                                                    i=item,
                                                    w=website,))

    print('')
    print("Shipping Cost = {}".format(model.Cost['Shipping'].value))
    print("Product Cost = {}".format(model.Cost['Item'].value))
    print('')

    for i in _results['Solution']:
        print("Total Cost = {}".format(i['Objective']['Objective']['Value']))


if __name__ == '__main__':

    from data import price, quantity, shipping

    model = ReferenceModel.create_model(price, quantity, shipping)

    display_results(solve_instance(model), model)
