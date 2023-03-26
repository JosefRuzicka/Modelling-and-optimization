import math
from multiprocessing import current_process
from webbrowser import get
import numpy as np
import re
from simplex_parser import *

def simplex(objective, restrictions, variables, maximize):
  obj_value = 0
  var_column = init_var_column(variables)
  CB_column = init_Cb_column(objective, variables, var_column)
  B_column = np.asarray(restrictions)[:,-1]

  # Step 0: set initial Zj and Z-Zj values.
  objective_np = np.array(objective).astype(np.float64)
  restrictions_np = np.array(restrictions).astype(np.float64)
  zj = calculate_zj(restrictions_np, len(variables), CB_column)
  
  # objective_np = z
  z_minus_zj = np.subtract(objective_np, zj).astype(np.float64)
  # Step 1: check Z-Zj in order to find if an optimal solution has been reached.
  while not is_optimal_solution(z_minus_zj, maximize):
    # Step 2: select pivot column.
    #pivot_column, pivot_column_index = get_pivot_column(restrictions, z_minus_zj, maximize)
    pivot_column, pivot_column_index = get_pivot_column(restrictions_np, z_minus_zj, maximize)

    # Step 3: select pivot row (and calculate ratios)
    #pivot_row, pivot_row_index       = get_pivot_row(restrictions, B_column, pivot_column)
    pivot_row, pivot_row_index       = get_pivot_row(restrictions_np, B_column, pivot_column)
    # Step 4: Gaussian reduction to make pivot cell == 1
    # Reduce pivot cell to 1.

    restrictions_np[pivot_row_index, :] = np.divide(restrictions_np[pivot_row_index, :], restrictions_np[pivot_row_index][pivot_column_index])

    # Gaussian reduction to make pivot column cells == 0
    for r in range(len(restrictions)):
      if r != pivot_row_index:
        restrictions_np[r, :] = np.subtract(restrictions_np[r, :], np.multiply(restrictions_np[pivot_row_index, :], restrictions_np[r, pivot_column_index]))
    B_column = restrictions_np[:, -1]
    
    # Change Var column and CB column.
    var_column[pivot_row_index] = variables[pivot_column_index]
    CB_column[pivot_row_index] = objective[pivot_column_index]

    # Calculate Z and Z-Zj.
    zj = calculate_zj(restrictions_np, len(variables), CB_column)
    # objective_np = z
    obj_value = calculate_objective_value(restrictions_np, CB_column)
    z_minus_zj = np.subtract(objective_np, zj).astype(np.float64)
    #print("ITERATION")
    #print("VAR COLUMN: ", var_column)
    #print("CB COLUMN: ", CB_column)
    #print("RESTRICTIONS: ", restrictions_np)
    #print("ZJ: ", zj)
    #print("Z-ZJ: ", z_minus_zj)
    #print("B COLUMN", B_column)
    #print("OBJECTIVE VALUE: ", obj_value)
  solution = []
  for index in range(len(var_column)):
    solution.append((var_column[index], B_column[index]))
  solution = (solution, obj_value)
  return solution

def init_Cb_column(objective, variables, var_column):
  Cb_column = np.zeros(len(var_column))
  for i in range (0, len(Cb_column)):
    # Search index of var_column(Slack/Artificial variable) in variables
    obj_i = variables.index(var_column[i])
    # Assign value to Cb_column
    Cb_column[i] = objective[obj_i]
  return Cb_column

# Assumes "s/S" for Slack variables and "a/A" for artificial variables
def init_var_column(variables):
  var_column = []
  for var in variables:
    if var[0] == "s" or var[0] == 'S':
      var_column.append(var)
    if var[0] == "a" or var[0] == 'A':
      slack_index = var_column.index("s" + var[1])
      var_column[slack_index] = var
  return var_column


def is_optimal_solution(z_minus_zj, maximize):
  is_optimal_solution = True  
  if maximize:
    # All values must be <= 0
    for i in z_minus_zj:
      if i > 0:
        is_optimal_solution = False
        break
  else:
    # All values must be >= 0
    for i in z_minus_zj:
      if i < 0:
        is_optimal_solution = False
        break
  return is_optimal_solution

def get_pivot_column(restrictions, z_minus_zj, maximize):
  if (maximize):
    pivot_column_index = np.argmax(z_minus_zj)
  else:
    pivot_column_index = np.argmin(z_minus_zj)

  pivot_column = np.asarray(restrictions)[:,pivot_column_index]
  return pivot_column, pivot_column_index

def get_pivot_row(restrictions, B_column, pivot_column):
  # Calculate division, ignoring values <= 0
  ratio_column = np.zeros(len(B_column)).astype(np.float64)
  ratio_column = np.divide(B_column, pivot_column, where=pivot_column!=0)
  # We set a high number to the ratio cells that were ignored.
  ratio_column[pivot_column <= 0] = '99999'

  # Pivot row selection
  pivot_row_index = np.argmin(ratio_column)
  pivot_row       = np.asarray(restrictions)[pivot_row_index,:]
  return pivot_row, pivot_row_index

def calculate_zj(restrictions_np, len_variables, Cb_column):
  zj = np.zeros(len_variables)
  for i in range(len_variables):
    multiplication = np.multiply(restrictions_np[:,i], Cb_column)
    zj[i] = np.sum(multiplication)
  return zj

def calculate_objective_value(restrictions_np, Cb_column):
  multiplication = np.multiply(restrictions_np[:,-1], Cb_column)
  obj_value = np.sum(multiplication)
  return obj_value

# For Testing Simplex
#simplex([30.0, 100.0, 0, 0, 0, -100000.0], 
#        [ 
#          [1, 1, 1, 0, 0, 0, 7.0],
#          [4.0, 10.0, 0, 1, 0, 0, 40.0],
#          [10.0, 0, 0, 0, -1, 1, 30.0]
#        ],
#        ['x1', 'x2', 's1', 's2', 's3', 'a3'],
#        True
#      )
#simplex([0.65,0.45,0,0,0],
#        [
#          [2,3,1,0,0, 400],
#          [3,1.5,0,1,0, 300],
#          [1,0,0,0,1, 90]
#        ],
#        ['x1', 'x2', 's1', 's2', 's3'],
#        True)
def simplex_solver(objective, restrictions, maximize):
  parsed_objective, parsed_restrictions, variables = parse_problem(objective, restrictions, maximize)
  solution = simplex(parsed_objective, parsed_restrictions, variables, maximize)
  return solution

