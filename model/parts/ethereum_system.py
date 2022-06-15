"""
# Ethereum System

General Ethereum mechanisms slimmed down to bare needs
"""

import typing
import datetime

from model import constants as constants
from model.types import ETH, USD_per_ETH, Gwei, Stage


# def policy_upgrade_stages(params, substep, state_history, previous_state):
#     """
#     ## Upgrade Stages Policy
#
#     Transitions the model from one stage in the Ethereum network
#     upgrade process to the next at different milestones.
#
#     This is essentially a finite-state machine: https://en.wikipedia.org/wiki/Finite-state_machine
#     """
#
#     # Parameters
#     dt = params["dt"]
#     stage: Stage = params["stage"]
#     date_start = params["date_start"]
#     date_eip1559 = params["date_eip1559"]
#     date_pos = params["date_pos"]
#
#     # State Variables
#     current_stage = previous_state["stage"]
#     timestep = previous_state["timestep"]
#
#     # Calculate current timestamp from timestep
#     timestamp = date_start + datetime.timedelta(
#         days=(timestep * dt / constants.epochs_per_day)
#     )
#
#     # Initialize stage State Variable at start of simulation
#     if current_stage is None:
#         current_stage = stage
#     else:
#         # Convert Stage enum value (int) to Stage enum
#         current_stage = Stage(current_stage)
#
#     # Stage finite-state machine
#     if stage == Stage.ALL:
#         # If Stage ALL selected, transition through all stages
#         # at different timestamps
#         if (
#             current_stage in [Stage.ALL, Stage.BEACON_CHAIN]
#             and timestamp < date_eip1559
#         ):
#             current_stage = Stage.BEACON_CHAIN
#         elif (
#             current_stage in [Stage.ALL, Stage.BEACON_CHAIN, Stage.EIP1559]
#             and timestamp < date_pos
#         ):
#             current_stage = Stage.EIP1559
#         else:
#             current_stage = Stage.PROOF_OF_STAKE
#     elif stage == Stage.BEACON_CHAIN:
#         # If Stage BEACON_CHAIN selected, only execute single stage
#         current_stage = Stage.BEACON_CHAIN
#     elif stage == Stage.EIP1559:
#         # If Stage EIP-1559 selected, only execute single stage
#         current_stage = Stage.EIP1559
#     elif stage == Stage.PROOF_OF_STAKE:
#         # If Stage PROOF_OF_STAKE selected, only execute single stage
#         current_stage = Stage.PROOF_OF_STAKE
#     else:
#         # Else, raise exception if invalid Stage
#         raise Exception("Invalid Stage selected")
#
#     return {
#         "stage": current_stage.value,
#         "timestamp": timestamp,
#     }

#
# def policy_network_issuance(
#     params, substep, state_history, previous_state
# ) -> typing.Dict[str, ETH]:
#     """
#     ## Network Issuance Policy Function
#
#     Calculate the total network issuance and issuance from Proof of Work block rewards.
#     """
#
#     # Parameters
#     dt = params["dt"]
#     daily_pow_issuance = params["daily_pow_issuance"]
#
#     # State Variables
#     stage = previous_state["stage"]
#     amount_slashed = previous_state["amount_slashed"]
#     total_base_fee = previous_state["total_base_fee"]
#     total_priority_fee_to_validators = previous_state[
#         "total_priority_fee_to_validators"
#     ]
#     total_online_validator_rewards = previous_state["total_online_validator_rewards"]
#
#     # Calculate network issuance in ETH
#     network_issuance = (
#         # Remove priority fee to validators which is not issuance (ETH transferred rather than minted)
#         (total_online_validator_rewards - total_priority_fee_to_validators)
#         - amount_slashed
#         - total_base_fee
#     ) / constants.gwei
#
#     # Calculate Proof of Work issuance
#     pow_issuance = (
#         daily_pow_issuance / constants.epochs_per_day
#         if Stage(stage) in [Stage.BEACON_CHAIN, Stage.EIP1559]
#         else 0
#     )
#     network_issuance += pow_issuance * dt
#
#     return {
#         "network_issuance": network_issuance,
#         "pow_issuance": pow_issuance,
#     }



def update_eth_price(
    params, substep, state_history, previous_state, policy_input
) -> typing.Tuple[str, USD_per_ETH]:
    """
    ## ETH Price State Update Function

    Update the ETH price from the `eth_price_process`.
    """

    # Parameters
    dt = params["dt"]
    eth_price_process = params["eth_price_process"]

    # State Variables
    run = previous_state["run"]
    timestep = previous_state["timestep"]

    # Get the ETH price sample for the current run and timestep
    eth_price_sample = eth_price_process(run, timestep * dt)

    return "eth_price", eth_price_sample

#
# def update_eth_supply(
#     params, substep, state_history, previous_state, policy_input
# ) -> typing.Tuple[str, ETH]:
#     """
#     ## ETH Supply State Update Function
#
#     Update the ETH supply from the Network Issuance Policy Function.
#     """
#
#     # Policy Inputs
#     network_issuance = policy_input["network_issuance"]
#
#     # State variables
#     eth_supply = previous_state["eth_supply"]
#
#     return "eth_supply", eth_supply + network_issuance
