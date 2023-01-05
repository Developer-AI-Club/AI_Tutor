# import required modules
import pandas as pd
import csv
# assign header columns
headerList = ['Word list', 'Tag', 'Time']

# open CSV file and assign header
with open("./data/training_data.csv", 'w') as file:
    dw = csv.DictWriter(file,
                        fieldnames=headerList, )
    dw.writeheader()