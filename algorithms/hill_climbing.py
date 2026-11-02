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
    def solve(self):
        problem = self.problem
        initial = problem.generate_initial_state()
        best, best_cost = initial, problem.evaluate(initial)
        self.history = []
        for restart in range(self.max_restarts+1):
            current = initial
            if restart:
                for _ in range(random.randint(1, 8)):
                    neighbors = get_neighbors(current, problem)
                    if neighbors:
                        current = random.choice(neighbors)
            sideways = 0
            visited = {current}
            while True:
                cost = problem.evaluate(current)
                if cost < best_cost:
                    best, best_cost = current, cost
                self.history.append(best_cost)
                neighbors = [s for s in get_neighbors(current, problem) if s not in visited]
                if not neighbors:
                    break
                scored = [(problem.evaluate(s), s) for s in neighbors]
                low = min(value for value, _ in scored)
                if low > cost + 1e-9:
                    break
                if abs(low-cost) < 1e-9:
                    if sideways >= self.max_sideways:
                        break
                    sideways += 1
                else:
                    sideways = 0
                current = random.choice([s for value,s in scored if abs(value-low)<1e-9])
                visited.add(current)
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
        
