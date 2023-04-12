from ortools.sat.python import cp_model
from itertools import combinations
import math
from lib import brackets

def optimize(nb_players, matches, groups, power):
    # Create the CP-SAT model
    model = cp_model.CpModel()

    # Define the player seeding variables. They are ordered and named as their
    # original seeding.
    variables = [model.NewIntVar(0, nb_players-1, str(i)) for i in range(nb_players)]

    # Add the constraint to ensure that each variable is assigned a unique value
    model.AddAllDifferent(variables)

    # We will now build the collide cost variable to minimize, as well as the deviation
    # cost. We shall manipulate ortools variable objects all along, which makes some
    # operations less straightforward.

    # Get the encounter probability matrix then flatten it and convert it to integers 
    # to be able to later use the array index constraint from ortools : AddElement
    m = brackets.build_encounter_prob_matrix(nb_players, matches)
    int_m = []
    for row in m:
        for el in row:
            int_m.append(int(el*100))

    # Create vars for each collide probability
    collide_costs = []
    for group, members in groups.items():
        for (x, y) in combinations(members, 2):
            collide_cost = model.NewIntVar(0, 100, f'({x},{y})')
            collide_costs.append(collide_cost)
            comb_index = model.NewIntVar(0, nb_players*nb_players-1, f'({x},{y})INDEX')
            model.Add(comb_index == variables[x] * nb_players + variables[y])
            model.AddElement(comb_index, int_m, collide_cost)

    # Create the total collide cost and define the minimize objective
    total_collide_cost = model.NewIntVar(0, 100*nb_players, 'total_collide_cost')
    model.Add(total_collide_cost == sum(collide_costs))
    model.Minimize(total_collide_cost)

    # This is used to ponderate deviation so that bad seeds deviations cost less
    # compared to good seeds deviations
    def deviation_factor(seed):
        return int(1000/(math.sqrt(seed+1)*nb_players))

    # Create vars for each player deviation
    deviation_costs = []
    for i in range(nb_players):
        # i is the original seeding
        deviation_cost = model.NewIntVar(-1000, 1000, f'{i} deviation')
        model.Add(deviation_cost == (variables[i] - i) * deviation_factor(i))
        abs_deviation_cost = model.NewIntVar(0, 1000, f'{i} abs deviation')
        model.AddAbsEquality(abs_deviation_cost, deviation_cost)
        deviation_costs.append(abs_deviation_cost)

    # Create the total deviation cost and define the constraint
    total_deviation_cost = model.NewIntVar(0, 1000000, 'total_deviation_cost')
    model.Add(total_deviation_cost == sum(deviation_costs))

    model.Add(total_deviation_cost < 100*power)

    # Add Hints (initial seeding) to speed up the process
    for i, xi in enumerate(variables):
        model.AddHint(xi, i)

    # Define the solver
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0

    # Solve the problem
    status = solver.Solve(model)

    # Return the solution
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {
            'deviation_score': solver.Value(total_deviation_cost),
            'alternative_seeding': {
                i: solver.Value(variables[i]) for i in range(nb_players)
            }
        }
    else:
        raise Exception('CP-SAT solver did not find a solution.')