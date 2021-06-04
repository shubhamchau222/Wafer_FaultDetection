# this file is for testing / rough only
import json
import os

# remove ''' to test this file

'''

# get the cwd
cwd = os.getcwd()
json_file_path = os.path.join(cwd , 'schema_training.json' )
print(json_file_path)

# dictionatry holding the json file values
a={}
# load json file and store the values
try:
    with open(json_file_path ) as data_file:
        a = json.load(data_file)

except Exception as e:
    print(e)
    print('IOerror')
    exit(1)

print(a.keys())  # all the data stored in dictionary a_
'''