"""
# Liquidiyt Bootstrapping Pool

LBP mechanisms for buybacks
"""

import typing
import datetime

from model import constants as constants
from model.types import ETH, USD_per_ETH, Gwei, Stage


def policy_upgrade_stages(params, substep, state_history, previous_state):
    """
    ## Upgrade Stages Policy
    """
    # Parameters
    dt = params["dt"]
    stage: Stage = params["stage"]
    date_start = params["date_start"]

    # State Variables
    current_stage = previous_state["stage"]
    timestep = previous_state["timestep"]


    # Calculate current timestamp from timestep
    timestamp = date_start + datetime.timedelta(
        days=(timestep * dt / constants.epochs_per_day)
    )

    # Initialize stage State Variable at start of simulation
    if current_stage is None:
        current_stage = stage
    else:
        # Convert Stage enum value (int) to Stage enum
        current_stage = Stage(current_stage)

    return {
        "stage": current_stage,
        "timestamp": timestamp,
    }

def policy_adjust_weight(params, substep, state_history, previous_state):
    """
    ## Adjust Weight Policy Function

    Adjust the weight of the LBP
    """

    # Parameters
    weight_x_start = params["weight_x_start"]
    weight_x_end = params["weight_x_end"]
    lbp_length = params["lbp_length"]

    # State Variables
    current_weight = previous_state["weight_x"]
    current_stage = previous_state["stage"]
    lbp_supply_x = previous_state['lbp_supply_x']


    if current_stage == Stage.LBP:
        # Do not adjust weight on initialization
        if current_weight is None:
            current_weight = weight_x_start
            # Determine new weight
        else:
            if weight_x_start > weight_x_end:
                adjustment_weight = (weight_x_start - weight_x_end) / lbp_length
                current_weight -= adjustment_weight
                if current_weight < weight_x_end:
                    current_weight = weight_x_end
            else:
                adjustment_weight = (weight_x_end - weight_x_start) / lbp_length
                current_weight += adjustment_weight
                if current_weight > weight_x_end:
                    current_weight = weight_x_end
    # else:
    #     # Else, raise exception if invalid Stage
    #     raise Exception("Invalid Stage selected")
    return {
        "weight_x": current_weight,
    }


def policy_add_liquidity(params, substep, state_history, previous_state):
    """
    ## Add Liquidity Policy Function

    Adds liquidity to pool
    """

    # Parameters
    lbp_initial_x = params['lbp_initial_x']
    lbp_initial_y = params['lbp_initial_y']
    weight_x_start = params["weight_x_start"]


    # State Variables
    current_stage = previous_state["stage"]
    weight_x = previous_state["weight_x"]
    timestep = previous_state["timestep"]
    lbp_supply_x = previous_state['lbp_supply_x']
    lbp_supply_y = previous_state['lbp_supply_y']
    # Stage finite-state machine
    if current_stage == Stage.LBP:
        if lbp_supply_x == 0:
            lbp_supply_x = lbp_initial_x
            lbp_supply_y = lbp_initial_y
    return {
        "lbp_supply_x": lbp_supply_x,
        "lbp_supply_y": lbp_supply_y,
    }

def policy_calc_pricing(params, substep, state_history, previous_state):
    """
    ## Calc Pricing Policy Function

    Gets current prices
    """

    # Parameters
    dt = params["dt"]
    stage: Stage = params["stage"]

    # State Variables
    current_stage = previous_state["stage"]
    weight_x = previous_state["weight_x"]
    timestep = previous_state["timestep"]
    lbp_supply_x = previous_state['lbp_supply_x']
    lbp_supply_y = previous_state['lbp_supply_y']
    eth_price = previous_state['eth_price']

    # Stage finite-state machine
    if current_stage == Stage.LBP:
        if lbp_supply_x == 0:
            lbp_supply_x = lbp_initial_x
            lbp_supply_y = lbp_initial_y

        weight_y = 1 - weight_x
        x_weighted = lbp_supply_x / weight_x
        y_weighted = lbp_supply_y / weight_y
        lbp_price_y_in_x = x_weighted / y_weighted
        lbp_price_x_in_y = y_weighted / x_weighted

        ## Assumes X is ETH
        lbp_y_usd_price = eth_price * lbp_price_y_in_x

    return {
        "lbp_price_y_in_x": lbp_price_y_in_x,
        "lbp_price_x_in_y": lbp_price_x_in_y,
        "lbp_y_usd_price": lbp_y_usd_price
    }

# def policy_buy_x(
#     params, substep, state_history, previous_state
# ) -> typing.Dict[str, ETH]:
#     """
#     ## Buy X Policy Function
#
#     Calculate the new X and Y balance of the pool
#     """
#     return {}
#
#
#
# def policy_sell_x(
#     params, substep, state_history, previous_state
# ) -> typing.Dict[str, ETH]:
#     """
#     ## Buy X Policy Function
#
#     Calculate the new X and Y balance of the pool
#     """
#     return {}
