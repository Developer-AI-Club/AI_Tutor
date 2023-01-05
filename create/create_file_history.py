# import required modules
import pandas as pd
import csv
# assign header columns
headerList = ['Request', 'Response', 'Time']

# open CSV file and assign header
with open("./data/history.csv", 'w') as file:
    dw = csv.DictWriter(file,
                        fieldnames=headerList)
    dw.writeheader()