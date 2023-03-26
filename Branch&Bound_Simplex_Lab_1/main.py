import Simplex

def main():
    # First test
    equation     = "0.65x1 + 0.45x2" 
    restrictions = ["2x1 + 3x2 <= 400",
                    "3x1 + 1.5x2 <= 300",
                    "x1 <= 90"],
    maximize     = True
    print(Simplex.simplex_solver(equation, restrictions, maximize))
    
    # Second test
    equation     = "30x1 + 100x2" 
    restrictions = ["x1 + x2 <= 7", 
                "4x1 + 10x2 <= 40", 
                "10x1 >= 30"],
    maximize     = True
    print(Simplex.simplex_solver(equation, restrictions, maximize))
    # Third test
    equation     = "3x1 + 8x2" 
    restrictions = ["x1 + 4x2 >= 3.5",
                    "x1 + 2x2 >= 2.5"],
    maximize     = False
    print(Simplex.simplex_solver(equation, restrictions, maximize))
    
if __name__ == "__main__":
    main()