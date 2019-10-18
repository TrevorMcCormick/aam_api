#' toDataFrame

def toDataFrame(file):
    if file.endswith('xlsx') or file.endswith('xls'):
        print('Creating pandas df from excel sheet.')
        traits = pd.read_excel(file)
    if file.endswith('csv'):
        print('Creating pandas df from csv.')
        traits = pd.read_csv(file)
    return(traits)
