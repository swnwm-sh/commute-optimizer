"""
algorithms/genetic_algorithm.py
Population-based optimization using selection, recombination, and mutation.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, crossover


class GeneticAlgorithmSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.population_size: int = self.params.get("population_size", 30)
        self.generations: int = self.params.get("generations", 100)
        self.crossover_rate: float = self.params.get("crossover_rate", 0.8)
        self.mutation_rate: float = self.params.get("mutation_rate", 0.2)
        self.elitism: int = self.params.get("elitism", 2)

    def solve(self) -> Tuple[State, float]:
                self.history = []
        size = max(2, int(self.population_size))
        elite_count = max(0, min(int(self.elitism), size))
        seed = self.problem.generate_initial_state()
        population = [seed]
        for _ in range(size-1):
            state = seed
            for _ in range(random.randint(1, 16)):
                options = get_neighbors(state, self.problem)
                if options:
                    state = random.choice(options)
            population.append(state)

        def fitness(state):
            cost = self.problem.evaluate(state)
            return 0.0 if cost == float('inf') else 1.0/(1.0+max(0.0,cost))

        def select():
            if self.selection_method.lower() in ('roulette', 'roulette_wheel'):
                return random.choices(population, weights=[fitness(s) for s in population], k=1)[0]
            contestants = random.sample(population, min(len(population), max(2, int(self.tournament_size))))
            return min(contestants, key=self.problem.evaluate)

        best = min(population, key=self.problem.evaluate)
        best_cost = self.problem.evaluate(best)
        self.history.append(best_cost)
        for _ in range(self.generations):
            population.sort(key=self.problem.evaluate)
            new_population = population[:elite_count]
            while len(new_population) < size:
                p1, p2 = select(), select()
                child = crossover(p1, p2, self.problem) if random.random() < self.crossover_rate else p1
                if random.random() < self.mutation_rate:
                    options = get_neighbors(child, self.problem)
                    if options:
                        child = random.choice(options)
                if not self.problem.is_valid_state(child):
                    child = seed
                new_population.append(child)
            population = new_population
            gen_best = min(population, key=self.problem.evaluate)
            gen_cost = self.problem.evaluate(gen_best)
            if gen_cost < best_cost:
                best, best_cost = gen_best, gen_cost
            self.history.append(best_cost)
        return best, best_cost
        """
        Executes Genetic Algorithm optimization.

        Guidelines:
        - Initialize a population of valid candidate solutions.
        - Design a fitness metric suitable for minimizing commute travel time (lower cost -> higher fitness).
        - Use selection operators (such as tournament or roulette selection) to pick parents.
        - Pair parents to produce offspring via `crossover()`, and apply stochastic mutation.
        - Preserve the top candidates across generations if using elitism.
        - Track best population performance per generation in self.history.

        Encouraged:
        - Experimenting with population size, selection pressure, and operator rates to balance exploration vs. exploitation.
        """
        
