import os
from image import Image

directory = 'Campus_pnm'
target = 'Campus_running_res'
bg = Image(filename=f'{directory}/trees1000.pnm').weighted_avg_gray()
for f in os.listdir(directory):
    curr = Image(filename=f'{directory}/{f}').weighted_avg_gray()
    res = curr.diff(bg, 90)
    bg = bg.update_running_back(curr, 0.05)
    res.write_to_file(f'{target}/{f}')
    print(f)
