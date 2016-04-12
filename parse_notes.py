'''
help('repr')
to find out exactly how python read input
'''
>>> with open ('CAD_RELEASED_VERSIONS.csv', 'r') as csvfile:
...     for line in csvfile:
...             print repr(line)
