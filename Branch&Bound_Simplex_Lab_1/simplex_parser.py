import re

def parse_equation(equation):
  # Dictionary of variables and their coefficients
  variables_dict = {}
  # Remove all white spaces to simplify regex
  equation = re.sub("\s+", "", equation)
  # Split variables and their coefficients
  variables = re.split("([+-]*\d*\.*\d*\w\d+)", equation)
  # Filter empty strings
  variables = list(filter(None, variables))
  # Store variables and coefficients in dictionary
  for var in variables:
    # Search coefficients in each variable
    coefficient = get_coefficient(var)
    # Search variable
    var = re.search("([a-zA-Z]\d+)", var)
    # Store in dictionary
    variables_dict[var.group()] = coefficient    
  return variables_dict

def get_coefficient(variable):
  coefficient = re.search("([+-]*\d*\.*\d*(?=[\w]))", variable)
  # Coefficient = 1
  if coefficient.group() == "+" or coefficient.group() == "":
    coefficient = float(1)
  # Coefficient = -1
  elif coefficient.group() == "-":
    coefficient = float(-1)
  # Coefficient != 1 AND != -1
  else:
    coefficient = float(coefficient.group())
  return coefficient

# For Testing parse_equation
#equation = "-3.8x1 + 5x2 - 2x3"
#print(parse_equation(equation))


def parse_restriction(restriction):
  restriction_tuple = ()
  # Parse equation
  equation = re.search(".*(?=(<=|>=))",restriction)
  if equation:
    equation = parse_equation(equation.group())
  # Get restriction value
  restriction_value = re.search("(?<=(<=|>=))\s*\d+", restriction)
  restriction_value = float(restriction_value.group())
  # Get if is upperbound(<=) or lowerbound(>=)
  is_upperbound = True
  if restriction.find(">=") != -1:
    # Is lowerbound
    is_upperbound = False
  # Store in tuple
  restriction_tuple = (equation, restriction_value, is_upperbound)
  
  return restriction_tuple

# For Testing parse_restriction
#restriction = "-3.8x1 + 5x2 - 2x3 <= 35"
#print(parse_restriction(restriction))

def parse_problem(objective, restrictions, maximize):
  # Parse objective equation
  coefficient_array = []
  variable_array = []
  parsed_objective = parse_equation(objective)

  # Get objective coefficients.
  for index, value in enumerate(parsed_objective.values()):
    coefficient_array.append(float(value))
    variable_array.append("x" + str(index + 1))

  parsed_restrictions = []
  # Get surplus and slack variables
  for index, restriction in enumerate(restrictions[0]):
    parsed_restrictions.append(parse_restriction(restriction))
    coefficient_array.append(0)
    variable_array.append("s" + str(index + 1))

  # Get artificial variables
  for index, restriction in enumerate(restrictions[0]):
    if parsed_restrictions[index][2] == False:
      if maximize:
        coefficient_array.append(-100000.0)
      else:
        coefficient_array.append(100000.0)
      variable_array.append("a" + str(index + 1))

  # Build simplex table
  simplex_table = []
  for restriction_index, restriction in enumerate(restrictions[0]):
    current_row = []
    for variable_index in range(len(variable_array) + 1):
      # Get variable coefficient
      coefficient = parsed_restrictions[restriction_index][0].get("x" + str(variable_index + 1))

      # Append coefficient
      if (coefficient):
        current_row.append(float(coefficient))

      # Append surplus and slack variables coefficient
      elif variable_index == (len(parsed_objective) + restriction_index):
        if parsed_restrictions[restriction_index][2]:
          current_row.append(1)
        else:
          current_row.append(-1)

      # Append restriction variable coefficients
      elif variable_index == len(variable_array):
        current_row.append(float(parsed_restrictions[restriction_index][1]))
    
      #  Append surplus and slack variables coefficient
      elif ((variable_index == (len(parsed_objective) + len(restrictions) + restriction_index)) and parsed_restrictions[restriction_index][2] == False):
        current_row.append(1)
      else:
        current_row.append(0)

    simplex_table.append(current_row)
  return coefficient_array, simplex_table, variable_array

# for Testing parse_problem
#equation     = "30x1 + 100x2" 
#restrictions = ["x1 + x2 <= 7", 
#                "4x1 + 10x2 <= 40", 
#                "10x1 >= 30"],
#maximize     = True
#print(parse_problem(equation, restrictions, maximize))