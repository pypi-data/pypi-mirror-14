"""pyGtoP custom exceptions."""

class NoSuchLigandError(Exception):
    """The exception raised if a specific ligand is requested which does not
    exist."""
    pass



class PropertyNotRequestedYetError(Exception):
    """The exception raised if a ligand's property is accessed before it has
    been explictly requested. If the property is not one which can be accessed
    from the web services, a standard AttributeError will be returned."""
    pass



class NoSuchTypeError(Exception):
    """The exception raised if a random ligand is requested of a type which does
    not exist."""
    pass
