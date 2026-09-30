EXPERIMENT_STEPS = [
    "Pick Up Container",
    "Open Container",
    "Use Spatula to Extract",
    "Close Container"
]

DAG = {
    0: [1],
    1: [2],
    2: [3],
    3: [4]
}

current_step = 0