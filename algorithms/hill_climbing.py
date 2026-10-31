"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


class HillClimbingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.max_sideways: int = self.params.get("max_sideways", 100)
        self.max_restarts: int = self.params.get("max_restarts", 5)

    def solve(self) -> Tuple[State, float]:
        self.history = []
        best = self.problem.generate_initial_state()
        best_cost = self.problem.evaluate(best)
        for restart in range(self.max_restarts + 1):
            current = best if restart == 0 else self.problem.generate_initial_state()
            if restart:
                # Random walks diversify restarts beyond the default initial state.
                for _ in range(random.randint(2, 14)):
                    options = get_neighbors(current, self.problem)
                    if not options:
                        break
                    current = random.choice(options)
            current_cost = self.problem.evaluate(current)
            sideways = 0
            visited_plateau = {current}
            while True:
                self.history.append(best_cost)
                if current_cost < best_cost:
                    best, best_cost = current, current_cost
                    self.history[-1] = best_cost
                neighbors = get_neighbors(current, self.problem)
                if not neighbors:
                    break
                scored = [(self.problem.evaluate(s), s) for s in neighbors]
                min_cost = min(cost for cost, _ in scored)
                if min_cost < current_cost - 1e-9:
                    choices = [s for cost, s in scored if abs(cost-min_cost)<1e-9]
                    current = random.choice(choices)
                    current_cost = min_cost
                    sideways = 0
                    visited_plateau = {current}
                elif abs(min_cost-current_cost)<1e-9 and sideways < self.max_sideways:
                    choices = [s for cost, s in scored if abs(cost-current_cost)<1e-9 and s not in visited_plateau]
                    if not choices:
                        break
                    current = random.choice(choices)
                    visited_plateau.add(current)
                    sideways += 1
                else:
                    break
        self.history.append(best_cost)
        return best, best_cost
        """
        Executes Hill Climbing optimization.

        Guidelines:
        - Search through the neighborhood greedily for candidates that minimize total travel time.
        - Handle flat local maxima / shoulders by allowing up to `max_sideways` non-improving steps.
        - Apply up to `max_restarts` to explore different starting basins.
        - Track the best objective cost seen at each major step in self.history.

        Prohibited:
        - Looping indefinitely on flat plateaus.
        """
        
