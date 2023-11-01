import json
import numpy as np
from math import sqrt

# test_dict = {"name": "jeff", "age": 22, "height": 2.2}

# json_test_data = json.dumps(test_dict)

# rtn_data = json.loads(json_test_data)

# print(rtn_data)
# print(type(rtn_data["height"]))

map_data: dict = {"env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1", "map_dimensions": 4}
env_map_unshaped: np.array = np.fromstring(map_data["env_map"], dtype=int, sep=",")
env_map_shaped: np.array = env_map_unshaped.reshape(map_data["map_dimensions"], -1)

combined_with_shape = np.fromstring(map_data["env_map"], dtype=int, sep=",").reshape(
    map_data["map_dimensions"], -1
)

print(env_map_unshaped)
print(env_map_unshaped.shape)
