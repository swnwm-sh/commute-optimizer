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
    def solve(self):
        problem = self.problem
        seed = problem.generate_initial_state()
        population = [seed]
        for _ in range(self.population_size-1):
            state = seed
            for _ in range(random.randint(1, 12)):
                neighbors = get_neighbors(state, problem)
                if neighbors:
                    state = random.choice(neighbors)
            population.append(state)
        def fitness(state):
            return 1/(1+problem.evaluate(state))
        def choose():
            if self.selection == 'roulette':
                return random.choices(population, weights=[fitness(s) for s in population], k=1)[0]
            return min(random.sample(population, min(3, len(population))), key=problem.evaluate)
        best = min(population, key=problem.evaluate)
        best_cost = problem.evaluate(best)
        self.history = [best_cost]
        for _ in range(self.generations):
            population.sort(key=problem.evaluate)
            next_population = population[:min(self.elitism, self.population_size)]
            while len(next_population) < self.population_size:
                a,b = choose(), choose()
                child = crossover(a,b,problem) if random.random() < self.crossover_rate else a
                if random.random() < self.mutation_rate:
                    ns = get_neighbors(child, problem)
                    if ns:
                        child = random.choice(ns)
                next_population.append(child)
            population = next_population
            candidate = min(population, key=problem.evaluate)
            if problem.evaluate(candidate) < best_cost:
                best, best_cost = candidate, problem.evaluate(candidate)
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
        
