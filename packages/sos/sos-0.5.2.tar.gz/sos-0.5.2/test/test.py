[1]
t = [0, 1]
n = [1000]
output_prefix = 'rnorm'
output_suffix = 'rds'
input: for_each = ['n', 't']
output: pattern = ['{output_prefix}_{_n}_{_t}.{output_suffix}']
run('''touch ${_output}''')

