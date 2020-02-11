import pandas as pd
import xlrd
def toDataFrame(file):
    if file.endswith('xlsx') or file.endswith('xls'):
        try:
            df = pd.read_excel(file, engine='python')
        except:
            df = pd.read_excel(file)
    if file.endswith('csv'):
        try:
            df = pd.read_csv(file, engine='python')
        except:
            df = pd.read_csv(file)
    return(df)
