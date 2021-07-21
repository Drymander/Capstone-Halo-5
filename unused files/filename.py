
fname = 'generated.py'
data = 5

with open(fname, 'w') as f:
    f.write('data = [{}]'.format(data))

import generated
print(generated.data)

print('test')
