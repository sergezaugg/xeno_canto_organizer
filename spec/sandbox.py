

import os
import shutil

path = 'd:/xc_real_projects/xc_experiment01/birdXX'
path_dest = 'd:/xc_real_projects/xc_experiment01/birdYY'

for pa in os.listdir(path):
    for pi in os.listdir(os.path.join(path, pa)):
        for pu in os.listdir(os.path.join(path, pa, pi, 'wave')):
            source = os.path.join(path, pa, pi, 'wave', pu)
            destination = os.path.join(path_dest, pa + '_' + pu)
            shutil.copy(source, destination)


