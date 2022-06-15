# -*- coding: utf-8 -*-
"""
Definition of System Parameters, their types, and default values.

By using a dataclass to represent the System Parameters:
* We can use types for Python type hints
* Set default values
* Ensure that all System Parameters are initialized
"""


import logging
import numpy as np
from dataclasses import dataclass
from datetime import datetime

import model.constants as constants
import experiments.simulation_configuration as simulation
from model.types import (
    Run,
    Timestep,
    Percentage,
    Gwei,
    Gas,
    Gwei_per_Gas,
    ETH,
    USD_per_epoch,
    Percentage_per_epoch,
    ValidatorEnvironment,
    List,
    Callable,
    Epoch,
    Stage,
)
from model.utils import default
from data.historical_values import (
    eth_price_mean,
    eth_block_rewards_mean,
)


# Configure validator environment distribution
# validator_environments = [
#     # Configure a custom validator environment using the following as a template:
#     # ValidatorEnvironment(
#     #     type="custom",
#     #     percentage_distribution=0.01,  # 1%
#     #     hardware_costs_per_epoch=0.0014,
#     #     cloud_costs_per_epoch=0,
#     #     third_party_costs_per_epoch=0,
#     # ),
#     ValidatorEnvironment(
#         type="diy_hardware",
#         percentage_distribution=0.37,
#         hardware_costs_per_epoch=0.0014,
#     ),
#     ValidatorEnvironment(
#         type="diy_cloud",
#         percentage_distribution=0.13,
#         cloud_costs_per_epoch=0.00027,
#     ),
#     ValidatorEnvironment(
#         type="pool_staas",
#         percentage_distribution=0.27,
#         third_party_costs_per_epoch=0.12,
#     ),
#     ValidatorEnvironment(
#         type="pool_hardware",
#         percentage_distribution=0.05,
#         hardware_costs_per_epoch=0.0007,
#     ),
#     ValidatorEnvironment(
#         type="pool_cloud",
#         percentage_distribution=0.02,
#         cloud_costs_per_epoch=0.00136,
#     ),
#     ValidatorEnvironment(
#         type="staas_full",
#         percentage_distribution=0.08,
#         third_party_costs_per_epoch=0.15,
#     ),
#     ValidatorEnvironment(
#         type="staas_self_custodied",
#         percentage_distribution=0.08,
#         third_party_costs_per_epoch=0.12,
#     ),
# ]



@dataclass
class Parameters:
    """System Parameters
    Each System Parameter is defined as:
    system parameter key: system parameter type = default system parameter value

    Because lists are mutable, we need to wrap each parameter list in the `default(...)` method.

    For default value assumptions, see the ASSUMPTIONS.md document.
    """

    # Time parameters
    dt: List[Epoch] = default([simulation.DELTA_TIME])
    """
    Simulation timescale / timestep unit of time, in epochs.

    Used to scale calculations that depend on the number of epochs that have passed.

    For example, for dt = 100, each timestep equals 100 epochs.

    By default set to constants.epochs_per_day (~= 225)
    """

    stage: List[Stage] = default([Stage.ALL])
    """
    Which stage or stages of the network upgrade process to simulate.

    By default set to ALL stage, which for time-domain analyses simulates
    the transition from the current network network upgrade stage at today's date onwards
    (i.e. the transition from the Beacon Chain Stage,
    to the EIP-1559 Stage, to the Proof-of-Stake Stage),
    whereas phase-space analyses simulate the current network upgrade stage
    providing a "snapshot" of the system state at this time.

    See model.types.Stage Enum for further documentation.
    """
    #
    date_start: List[datetime] = default([datetime.now()])
    """Start date for simulation as Python datetime"""

    # date_eip1559: List[datetime] = default(
    #     [datetime.strptime("2021/08/04", "%Y/%m/%d")]
    # )
    # """
    # Expected EIP-1559 activation date as Python datetime.
    # """
    #
    # date_pos: List[datetime] = default([datetime.strptime("2021/12/1", "%Y/%m/%d")])
    # """
    # Eth1/Eth2 merge date as Python datetime, after which POW is disabled and POS is enabled.
    # """

    # Environmental processes
    eth_price_process: List[Callable[[Run, Timestep], ETH]] = default(
        [lambda _run, _timestep: eth_price_mean]
    )
    """
    A process that returns the ETH spot price at each epoch.

    By default set to average ETH price over the last 12 months from Etherscan.
    """

    weight_x_start: List[Percentage] = default(0.95)
    weight_x_end: List[Percentage] = default(0.30)
    lbp_length: List[int]      = default(100)
    lbp_initial_x: List[float] = default(100)
    lbp_initial_y: List[float] = default(10000)



# Initialize Parameters instance with default values
parameters = Parameters().__dict__
