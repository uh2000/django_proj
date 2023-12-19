import matplotlib.pyplot as plt
from sympy import *
import sympy
import numpy as np
import random
import math

class Graph_free_market:
    def __init__(self) -> None:
        pass
        
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    
    
    def market_graph(self, supply: str, demand: str, complete = False) -> None:
        price = self.get_price(supply, demand)
        quantity = self.get_quantity(supply, demand)
        
        start = 0
        if "x" in demand:
            end = self.get_zero_point(demand)
        else:
            end = 2 * quantity
        step = 1 
        

        if "x" in supply:
            supply_dict = self.get_calculate_values(supply, end)
            plt.plot(supply_dict.keys(),supply_dict.values(), label = "Supply") 
            
        else:
            supply_list = [price for i in range(start, end, step)]
            plt.plot(supply_list, label = "Supply") 
            
        
        if "x" in demand:
            demand_dict = self.get_calculate_values(demand, end)
            plt.plot(demand_dict.keys(),demand_dict.values(), label = "Demand") 
            
        else:
            demand_list = [price for i in range(start, end, step)]
            plt.plot(demand_list, label = "Demand") 
            

        plt.xlabel("Quantity")
        plt.ylabel("Price")
        
        if complete == True:
            plt.plot([i for i in range(0, round(quantity) + 1)], [price for i in range(0, round(quantity) + 1)],
                     linestyle = "dashed", label = f"Price*: {price}")
            plt.plot([quantity for i in range(0, round(price) + 1 )], [i for i in range(0,round(price) + 1)],
                     linestyle = "dashed", label = f"Quantity*: {quantity}")
            
            if "x" in demand:
                y1 = list(demand_dict.values())
            else:
                y1 = demand_list
            
            if "x" in supply:
                y2 = list(supply_dict.values())
            else:
                y2 = supply_list
            x = np.array([i for i in range(math.floor(quantity))]) + float(quantity)
            y1 = np.array(y1[0 : math.floor(quantity)], dtype=float) + float(quantity)
            y2 = np.array(y2[0 : math.floor(quantity)], dtype=float) + float(quantity)
            price_curve = np.array([price for i in range(len(x))], dtype=float)
            
            #print(y1, price_curve, x)
            plt.fill_between(x,y1,price_curve, where=(y1 >= price_curve), color='C0', alpha=0.9)
            plt.fill_between(x, y2, price_curve, where= (y2 <= price_curve), color = "C1", alpha=0.9)
            plt.text(float(quantity/4), price + 1, "Consumer\nsurplus")
            plt.text(float(quantity/4), price - 1, "Producer\nsurplus")
            

        plt.legend() 
        plt.show()


    def get_calculate_values(self, expression: str, end: int) -> dict:
        start = 0
        step = 1 
        
        value_pairs = {}
        equation_function = self.create_equation_function(expression)
        if equation_function:
            x_values = [i for i in range(start, end, step)]
            for x_val in x_values:
                result = equation_function(x_val)
                value_pairs[x_val] = result
                
               # print(f"For x = {x_val}, the result is {result}")

        else:
            print("Error: Unable to create the equation function.")
        return value_pairs    
    
    def create_equation_function(self, equation_str: str) -> str:
        x = symbols('x')
        
        try:
            equation = parse_expr(equation_str)
            equation_function = lambda x_val: equation.subs(x, x_val)
            return equation_function
        except Exception as e:
            return None

    def get_zero_point(self, expression: str) -> float:
        x = symbols('x')
        
        # Create the equation from the supply and demand functions
        equation = parse_expr(expression)
        
        # Calculate the equilibrium price and quantity
        zero_point = max(solve(equation, x))
        #print(zero_point)
        return round(zero_point)
    
    
    def get_quantity(self, supply: str, demand: str) -> float:
        x = symbols('x')
        
        # Create the equation from the supply and demand functions
        supply_eq = parse_expr(supply)
        demand_eq = parse_expr(demand)
        
        # Calculate the equilibrium price and quantity
        quantity = max(solve(Eq(supply_eq, demand_eq), x))
        #print(quantity)
        return quantity
    

    def get_price(self, supply: str, demand: str) -> float:
        x, y = symbols('x y')
        quantity = self.get_quantity(supply, demand)
        
        if "x" in demand:
            end = self.get_zero_point(demand)
        else:
            end = 2 * quantity
            
        # Create the equation from the supply and demand functions
        """ supply_eq = parse_expr(supply)
        demand_eq = parse_expr(demand) """
        
        equation_function = self.create_equation_function(demand)
        
        
        if "x" not in supply:
            price = float(supply)
        elif "x" not in demand:
            price = float(demand)
        else:
            price = equation_function(quantity)
             
        print(price)
        return price


    def get_consumer_surplus(self, supply: str, demand: str) -> float:
        x, y = symbols('x y')
        
        # Create the equation from the supply and demand functions
        """ supply_eq = parse_expr(supply)
        demand_eq = parse_expr(demand) """
        
        # Calculate the equilibrium price and quantity
        price = self.get_price(supply, demand)
        quantity = self.get_quantity(supply, demand)
        
        # Define the inverse demand function (price as a function of quantity)
        consumer_surplus = parse_expr(f"{demand}-{price}")
        
        # Calculate consumer surplus
        surplus = sympy.integrate(consumer_surplus, (x, 0, quantity)) 
        
        return surplus
    

    def get_producer_surplus(self, supply: str, demand: str) -> float:
        x, y = symbols('x y')
        
        # Create the equation from the supply and demand functions
        supply_eq = parse_expr(supply)
        demand_eq = parse_expr(demand)
        
        # Calculate the equilibrium price and quantity
        price = self.get_price(supply, demand)
        quantity = self.get_quantity(supply, demand)
        
        # Define the inverse demand function (price as a function of quantity)
        if "x" in supply:
            inverse_supply = solve(supply_eq - y, x)[0]
        else:
            inverse_supply = parse_expr(f"{supply}")
            
        if "x" in demand:    
            inverse_demand = solve(demand_eq - y, x)[0]
        else:
            inverse_demand = parse_expr(f"{demand}")
            

        producer_surplus = parse_expr(f"{price}-{inverse_supply}")
        
        # Calculate consumer surplus
        surplus = sympy.integrate(producer_surplus, (y, 0, quantity)) 
        
        return surplus


    def get_economic_surplus(self, supply: str, demand: str) -> float:
        consumer = self.get_consumer_surplus(supply, demand)
        producer = self.get_producer_surplus(supply, demand)
        economic_surplus = consumer + producer
        return economic_surplus
    
    
    
if __name__ == "__main__":
    
    for i in range(0, 3):
        a = random.randint(0,5)
        b = random.randint(5,10)
        c = random.randint(0,5)
        d = random.randint(0,1)
        
        graph = Graph_free_market()
        supply_function = f"{a}*x + {d}"
        demand_function = f"{b} - {c}*x"
        
        print(f"supply function {supply_function}\ndemand function {demand_function}")
        
        consumer_surplus = graph.get_consumer_surplus(supply_function, demand_function)
        print("Consumer Surplus:", consumer_surplus)

        producer_surplus = graph.get_producer_surplus(supply_function, demand_function)
        print("Producer Surplus:", producer_surplus)

        economic_surplus = graph.get_economic_surplus(supply_function, demand_function)

        print("Economic Surplus:", economic_surplus)
        
        graph.market_graph(supply_function, demand_function, complete=True)
        
        price = graph.get_price(supply_function, demand_function)
        quantity = graph.get_quantity(supply_function, demand_function)
        print(f"Price: {price}, Quantity: {quantity}")
        
        """ graph = Graph_monopoly()
        supply = "2"
        demand = "50 -  x**2"
        graph.market_graph(supply, demand,0, 12, 1, complete=True, is_tot_cost = False) """
        