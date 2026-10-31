"""
algorithms/beam_search.py
Local Beam Search maintaining K parallel candidate states.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


class LocalBeamSearchSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.beam_width: int = self.params.get("beam_width", 5)
        self.max_iterations: int = self.params.get("max_iterations", 150)

    def solve(self) -> Tuple[State, float]:
                self.history = []
        width = max(1, int(self.beam_width))
        initial = self.problem.generate_initial_state()
        pool = {initial}
        frontier = [initial]
        for _ in range(width * 5):
            options = get_neighbors(random.choice(frontier), self.problem)
            if options:
                candidate = random.choice(options)
                pool.add(candidate)
                frontier.append(candidate)
        beam = sorted(pool, key=self.problem.evaluate)[:width]
        best = min(beam, key=self.problem.evaluate)
        best_cost = self.problem.evaluate(best)
        self.history.append(best_cost)
        for _ in range(self.max_iterations):
            candidates = set(beam)
            for state in beam:
                candidates.update(get_neighbors(state, self.problem))
            ranked = sorted(candidates, key=self.problem.evaluate)
            next_beam = ranked[:width]
            current_best = self.problem.evaluate(next_beam[0])
            if current_best < best_cost:
                best, best_cost = next_beam[0], current_best
            self.history.append(best_cost)
            if set(next_beam) == set(beam):
                break
            beam = next_beam
        return best, best_cost
        """
        Executes Local Beam Search.

        Guidelines:
        - Maintain a set of `beam_width` parallel configurations.
        - In each iteration, generate neighbors from all active states in the beam.
        - Pool and rank all generated successors collectively, then retain the top `beam_width` states.
        - Halt when the beam ceases to improve or reaches max_iterations.
        - Record the best cost of the population at each step in self.history.

        Encouraged:
        - Ensuring diversity across states in the beam to prevent collapse into a single redundant path.

        Prohibited:
        - Treating this as K independent, non-communicating searches.
        """
      
        
