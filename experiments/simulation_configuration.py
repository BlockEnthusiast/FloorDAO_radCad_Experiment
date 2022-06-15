"""
Simulation configuration such as the number of timesteps and Monte Carlo runs
"""

from model.constants import epochs_per_month, epochs_per_day


DELTA_TIME = epochs_per_day / 24  # epochs per timestep
SIMULATION_TIME_DAYS = 5  # number of days
TIMESTEPS = int(
    epochs_per_day * SIMULATION_TIME_DAYS // DELTA_TIME
)  # number of simulation timesteps
MONTE_CARLO_RUNS = 1  # number of runs
