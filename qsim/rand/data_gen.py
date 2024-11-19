import os
import sys

import numpy as np

rng = np.random.default_rng(0)
for q in [10, 20, 40, 60, 80, 100]:
    for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        support = int(q * p)
        if support == 0:
            support = 1
        for i in range(10):
            str_list = []
            for j in range(100):
                str_i = ""
                index = rng.choice(q, support, replace=False)
                for k in range(q):
                    if k in index:
                        str_i += rng.choice(["X", "Y", "Z"])
                    else:
                        str_i += "I"
                str_list.append(str_i)
            file_dir = "q" + str(q) + "_10" + "_p" + str(p)
            os.makedirs(file_dir, exist_ok=True)
            file_name = file_dir + "/i" + str(i) + ".txt"
            with open(file_name, "w") as f:
                f.write(str(str_list))
