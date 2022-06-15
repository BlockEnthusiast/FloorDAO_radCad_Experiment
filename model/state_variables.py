import numpy as np
from dataclasses import dataclass
from datetime import datetime

import model.constants as constants
import data.api.beaconchain as beaconchain
import data.api.etherscan as etherscan
import model.system_parameters as system_parameters

# from model.system_parameters import validator_environments
from model.types import (
    Gwei,
    Gwei_per_Gas,
    ETH,
    USD,
    USD_per_ETH,
    Percentage,
    Stage,
)
from data.historical_values import eth_price_mean, eth_price_min, eth_price_max

# Initial state from external live data source, setting a default in case API call fails
eth_supply: ETH = etherscan.get_eth_supply(default=116_250_000e18) / constants.wei


@dataclass
class StateVariables:
    """State Variables
    Each State Variable is defined as:
    state variable key: state variable type = default state variable value
    """

    # Time state variables
    stage: Stage = None
    """
    The stage of the network upgrade process.

    See "stage" System Parameter in model.system_parameters
    & model.types.Stage Enum for further documentation.
    """
    timestamp: datetime = None
    """
    The timestamp for each timestep as a Python `datetime` object, starting from `date_start` Parameter.
    """

    # Ethereum state variables
    eth_price: USD_per_ETH = eth_price_mean
    """The ETH spot price"""
    # eth_supply: ETH = eth_supply
    # """The total ETH supply"""
    # eth_staked: ETH = eth_staked
    # """The total ETH staked as part of the Proof of Stake system"""
    # supply_inflation: Percentage = 0
    # """The annualized ETH supply inflation rate"""
    # network_issuance: ETH = 0
    # """The total network issuance in ETH"""
    # pow_issuance: ETH = 0
    # """The total Proof of Work issuance in ETH"""

    # LBP state Variables
    weight_x: Percentage = None
    lbp_supply_x: float = 0
    lbp_supply_y: float = 0
    lbp_price_x_in_y: float = 0
    lbp_price_y_in_x: float = 0
    lbp_y_usd_price: float = 0





# Initialize State Variables instance with default values
initial_state = StateVariables().__dict__
