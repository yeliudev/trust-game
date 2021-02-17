# -----------------------------------------------------
# Trust Game
# Licensed under the MIT License
# Written by Ye Liu (ye-liu at whu.edu.cn)
# -----------------------------------------------------

cfg = {
    # Initial number of coins the user has
    'initial_coins': 100,

    # Number of total rounds
    'num_rounds': 10,

    # Multiplier for the money recieved by the trustee
    'multiplier': 3,

    # Agent Settings
    'agent': {
        # Whether to use the same gender as user
        'use_same_gender': True,

        # Whether to use the same ethnic as user
        'use_same_ethnic': True,

        # The potential means of yield rates of agents
        'means': [-0.8, -0.4, 0, 0.4, 0.8],

        # The potential variances of yield rates of agents
        'variances': [1, 1.5, 2],
    }
}
