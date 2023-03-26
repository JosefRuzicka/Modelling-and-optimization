import Simplex

# Branch and bound.
# Root.
equation     = "x1 + 4x2"
restrictions = ["-10x1 + 20x2 <= 22",
                "5x1 + 10x2 <= 49",
			    "x1 <= 5"],
maximize     = True
print(Simplex.simplex_solver(equation, restrictions, maximize))
# Result = ([('x2', 3.0), ('x1', 3.8), ('s3', 1.2000000000000002)], 15.8)

# Root-Left
# on x1 <= 3.
restrictions = ["-10x1 + 20x2 <= 22",
                "5x1 + 10x2 <= 49",
			    "x1 <= 5",
                "x1 <= 3"],
print(Simplex.simplex_solver(equation, restrictions, maximize))
# Result = ([('x2', 2.6), ('s2', 8.0), ('s3', 2.0), ('x1', 3.0)], 13.4)

# Root-Left-Left
# on x2 <= 2
restrictions = ["-10x1 + 20x2 <= 22",
                "5x1 + 10x2 <= 49",
			    "x1 <= 5",
                "x1 <= 3",
                "x2 <= 2"],
print(Simplex.simplex_solver(equation, restrictions, maximize))
# Result = ([('x2', 2.0), ('s2', 14.0), ('s3', 2.0), ('s1', 12.000000000000002), ('x1', 3.0)], 11.0)
# new optimal solution.

# Root-Left-Right
# On x2 >= 3
restrictions = ["-10x1 + 20x2 <= 22",
                "5x1 + 10x2 <= 49",
			    "x1 <= 5",
                "x1 <= 3",
                "x2 >= 3"],
# Infeasible solution.

# Root-Right
# On x1 >= 4
restrictions = ["-10x1 + 20x2 <= 22",
                "5x1 + 10x2 <= 49",
			    "x1 <= 5",
                "x1 >= 4"],
print(Simplex.simplex_solver(equation, restrictions, maximize))
# Result = ([('s1', 4.0), ('x2', 2.9), ('s3', 1.0), ('x1', 4.0)], 15.6)

# Root-Right-Left
# On x2 <= 2
restrictions = ["-10x1 + 20x2 <= 22",
                "5x1 + 10x2 <= 49",
			    "x1 <= 5",
                "x1 >= 4",
                "x2 <= 2"],
print(Simplex.simplex_solver(equation, restrictions, maximize))
# Result = ([('s1', 32.0), ('s2', 4.0), ('s4', 1.0), ('x1', 5.0), ('x2', 2.0)], 13.0
# New Optimal solution.

# Root-Right-Right
# On x2 >= 3 
restrictions = ["-10x1 + 20x2 <= 22",
                "5x1 + 10x2 <= 49",
			    "x1 <= 5",
                "x1 >= 4",
                "X2 >= 3"],
# Infeasible solution.

# Additional effort at an attempt at making a fully automatic Branch and Bound function.
'''
def simplex_solver(objective, restrictions, maximize):
  parsed_objective, parsed_restrictions, variables = parse_problem(objective, restrictions, maximize)
  solution = simplex_recursive(parsed_objective, parsed_restrictions, variables, maximize)
  print(solution)
  return solution

def simplex_recursive(parsed_objective, parsed_restrictions, variables, maximize):
  solution = simplex(parsed_objective, parsed_restrictions, variables, maximize)
  variable_selected = False
  # For each variable result, check if its an integer, if so: Branch and Bound. 
  for x in range(solution[0]):
    if (not solution[0].values[x].is_integer() and not variable_selected):
      variable_selected = True
      
      # Get int coefficients.
      new_variables_floor = variables
      new_variables_ceil  = variables
      new_variables_floor[x] = math.floor(solution[0].values[x])
      new_variables_ceil[x] = math.ceil(solution[0].values[x])
      
      # Add restrictions
        # Floor restriction:
      new_floor_restriction = "" + solution[0].keys[x] + " >= " + new_variables_floor[x]
      new_parsed_floor_restriction = parse_restriction(new_floor_restriction)
      floor_parsed_restrictions = parsed_restrictions
      floor_parsed_restrictions.append(new_parsed_floor_restriction)
      new_solution_floor = simplex_recursive(parsed_objective, floor_parsed_restrictions, new_variables_floor, maximize)
        # Ceil restriction:
      new_ceil_restriction  = "" + solution[0].keys[x] + " <= " + new_variables_ceil[x] 
      new_parsed_ceil_restriction = parse_restriction(new_ceil_restriction)
      ceil_parsed_restrictions = parsed_restrictions
      ceil_parsed_restrictions.append(new_parsed_ceil_restriction)
      new_solution_ceil = simplex_recursive(parsed_objective, ceil_parsed_restrictions, new_variables_ceil, maximize)

      # Find best solution.
      if (maximize):
        if (new_solution_floor[1] >= solution[1]):
          solution = new_solution_floor
        if (new_solution_ceil[1] >= solution[1]):
          solution = new_solution_ceil
      else:
        if (new_solution_floor[1] <= solution[1]):
          solution = new_solution_floor
        if (new_solution_ceil[1] <= solution[1]):
          solution = new_solution_ceil
  return solution
  '''