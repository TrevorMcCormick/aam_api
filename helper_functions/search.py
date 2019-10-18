#' search

def search(df, column, type, keywords):
    if type=="any":
        result = df[column].apply(lambda sentence: any(keyword in sentence for keyword in keywords))
        df = df[result]
    elif type=="all":
        result = df[column].apply(lambda sentence: all(keyword in sentence for keyword in keywords))
        df = df[result]
    return(df)
