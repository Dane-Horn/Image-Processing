import os

directory = 'Campus.1'
for f in os.listdir(directory):
    os.system(f'nconvert -out ppm {directory}/{f}')
    os.remove(f'{directory}/{f}')
    f = f.replace('.bmp', '.ppm')
    os.system(f'nconvert -ascii {directory}/{f}')
    os.remove(f'{directory}/{f}')
