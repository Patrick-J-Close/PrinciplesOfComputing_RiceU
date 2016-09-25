# http://www.codeskulptor.org/#user42_OYFdchqfIC_2.py

"""
Simulator for greedy boss scenario
"""

import simpleplot
import math
import codeskulptor
codeskulptor.set_timeout(20)

STANDARD = True
LOGLOG = False

# constants for simulation
INITIAL_SALARY = 100
SALARY_INCREMENT = 100
INITIAL_BRIBE_COST = 1000


def greedy_boss(days_in_simulation, bribe_cost_increment, plot_type = STANDARD):
    """
    Simulation of greedy boss
    """
    
    # initialize necessary local variables
    curr_salary = INITIAL_SALARY
    bribe_cost = INITIAL_BRIBE_COST
    curr_day = 0
    total_salary_earned = 0
    curr_acct = 0     
    
    # define  list consisting of days vs. total salary earned for analysis
    days_vs_earnings = []

    # Each iteration of this while loop simulates one bribe
    while curr_day <= days_in_simulation:
        
        # update list with days vs total salary earned
        # use plot_type to control whether regular or log/log plot
        if plot_type == STANDARD:
            days_vs_earnings.append((curr_day, total_salary_earned))
        elif plot_type == LOGLOG:
            days_vs_earnings.append([math.log(curr_day), math.log(total_salary_earned)])
        
        # check whether we have enough money to bribe without waiting
        if curr_acct >= bribe_cost:
            days_to_bribe = 0
        else:
            days_to_bribe = int(math.ceil((bribe_cost - curr_acct)/float(curr_salary)))
            
        # advance current_day to day of next bribe (DO NOT INCREMENT BY ONE DAY)
        curr_day += days_to_bribe
        
        # update state of simulation to reflect bribe
        total_salary_earned += days_to_bribe * curr_salary
        curr_acct += days_to_bribe * curr_salary
        curr_acct -= bribe_cost
        bribe_cost += bribe_cost_increment
        curr_salary += SALARY_INCREMENT
   
    return days_vs_earnings


def run_simulations():
    """
    Run simulations for several possible bribe increments
    """
    plot_type = LOGLOG
    days = 70
    inc_0 = greedy_boss(days, 0, plot_type)
    inc_500 = greedy_boss(days, 500, plot_type)
    inc_1000 = greedy_boss(days, 1000, plot_type)
    inc_2000 = greedy_boss(days, 2000, plot_type)
    simpleplot.plot_lines("Greedy boss", 600, 600, "days", "total earnings", 
                          [inc_0, inc_500, inc_1000, inc_2000], False,
                         ["Bribe increment = 0", "Bribe increment = 500",
                          "Bribe increment = 1000", "Bribe increment = 2000"])

run_simulations()

print greedy_boss(35, 100)
# should print [(0, 0), (10, 1000), (16, 2200), (20, 3400), (23, 4600), (26, 6100), (29, 7900), (31, 9300), (33, 10900), (35, 12700)]

print greedy_boss(35, 0)
# should print [(0, 0), (10, 1000), (15, 2000), (19, 3200), (21, 4000), (23, 5000), (25, 6200), (27, 7600), (28, 8400), (29, 9300), (30, 10300), (31, 11400), (32, 12600), (33, 13900), (34, 15300), (34, 15300), (35, 16900)]


            
            
    

