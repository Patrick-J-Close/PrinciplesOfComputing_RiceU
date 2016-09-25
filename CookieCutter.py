# http://www.codeskulptor.org/#user42_AMvoaRfdyy_16.py

"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
INITIAL_CPS = 1.0
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._game_time = 0.0
        self._current_cps = INITIAL_CPS
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "total cookies: " + str(self._total_cookies) + "\n" \
                "current cookies: " + str(self._current_cookies) + "\n" \
                "current time: " + str(self._game_time) + "\n" \
                "current CPS: " + str(self._current_cps) + "\n"
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._game_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies) / self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0: 
            pass
        else:
            self._game_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies += time * self._current_cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self._current_cookies:
            pass
        else:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._game_time, item_name, cost, self._total_cookies))
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    clone_build_info = build_info.clone()
    new_click = ClickerState()
    
    while 0 <= duration:
        item = strategy(new_click.get_cookies(), new_click.get_cps(), \
                       new_click.get_history(), duration, clone_build_info) 
        if item == None:
            break
        item_cost = clone_build_info.get_cost(item)
        wait_time = new_click.time_until(item_cost)
        
        if wait_time > duration:
            # item will not be avaialable until simulation is complete 
            break
        else:
            new_click.wait(wait_time)
            new_click.buy_item(item, item_cost, clone_build_info.get_cps(item))
            duration -= wait_time
            clone_build_info.update_item(item)
        
    new_click.wait(duration)
        
    return new_click


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = {}
    name = None
    
    for item in build_info.build_items():
        items[item] = build_info.get_cost(item)
    cheapest = min(items.values())
    
    if cheapest <= cookies + time_left * cps:
        for name, cost in items.items():
            if cost == cheapest:
                return name

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    max_cookies = cookies + cps * time_left
    items = build_info.build_items()
    name = None
    expensive = float('-inf')
    
    for item in build_info.build_items():
        temp_cost = build_info.get_cost(item)
        
        if temp_cost > expensive and temp_cost < max_cookies:
            expensive = temp_cost
            name = item
            
    return name

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return random.choice(build_info.build_items())
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("None", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
    

