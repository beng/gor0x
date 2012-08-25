def msg(*args): 
    """Print out message with variables
    Usage: msg('text',variable,...)"""
    return "".join(str(x) for x in args)


msg = Str("I found ", filecount, " files in ", foldercount, " directories" )