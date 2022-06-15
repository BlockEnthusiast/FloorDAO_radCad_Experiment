"""
cadCAD model State Update Block structure, composed of Policy and State Update Functions
"""

import model.parts.ethereum_system as ethereum
import model.parts.lbp_system as lbp
from model.system_parameters import parameters
from model.utils import update_from_signal



state_update_block_ethereum = {
    "description": """
        Environmental Ethereum processes:
        * ETH price update
    """,
    "policies": {
    },
    "variables": {
        "eth_price": ethereum.update_eth_price,
    },
}

state_update_block_stages =     {
    "description": """
        Update Stages
    """,
    "policies": {
        "policy_upgrade_stages": lbp.policy_upgrade_stages,
    },
    "variables": {
        "stage": update_from_signal(
            "stage"
        ),
        "timestamp": update_from_signal(
            "timestamp"
        ),
    },
}

_state_update_blocks = [
    {
        "description": """
            Adjust LBP Weight
        """,
        "policies": {
            "policy_adjust_weight": lbp.policy_adjust_weight,
        },
        "variables": {
            "weight_x": update_from_signal(
                "weight_x"
            ),
        },
    },
    {
        "description": """
            Adjust LBP Supply
        """,
        "policies": {
            "policy_add_liquidity": lbp.policy_add_liquidity,
        },
        "variables": {
            "lbp_supply_x": update_from_signal(
                "lbp_supply_x"
            ),
            "lbp_supply_y": update_from_signal(
                "lbp_supply_y"
            ),
        },
    },
    {
        "description": """
            Calc LBP Price
        """,
        "policies": {
            "policy_calc_pricing": lbp.policy_calc_pricing,
        },
        "variables": {
            "lbp_price_y_in_x": update_from_signal(
                "lbp_price_y_in_x"
            ),
            "lbp_price_x_in_y": update_from_signal(
                "lbp_price_x_in_y"
            ),
            "lbp_y_usd_price": update_from_signal(
                "lbp_y_usd_price"
            ),
        },
    },
]



# Conditionally update the order of the State Update Blocks using a ternary operator
_state_update_blocks = (
    # If driving with environmental ETH staked process, structure as follows:
    [
        state_update_block_ethereum,
        state_update_block_stages,
    ]
    + _state_update_blocks
    # if parameters["eth_staked_process"][0](0, 0) is not None
    # # Otherwise, if driving with validator adoption (implied ETH staked) process, switch Ethereum and validator blocks:
    # else [
    #     state_update_block_stages,
    #     state_update_block_validators,
    #     state_update_block_ethereum,
    # ]
    # + _state_update_blocks
)

# Split the state update blocks into those used during the simulation (state_update_blocks)
# and those used in post-processing to calculate the system metrics (post_processing_blocks)
state_update_blocks = [
    block for block in _state_update_blocks if not block.get("post_processing", False)
]
post_processing_blocks = [
    block for block in _state_update_blocks if block.get("post_processing", False)
]
