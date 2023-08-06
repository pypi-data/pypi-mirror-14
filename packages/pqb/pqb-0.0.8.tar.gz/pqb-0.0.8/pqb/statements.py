#encoding=utf-8
class LimitStatement(object):
    """
    Crea la sentencia LIMIT
    """ 
    def __init__(self, n):
        super(LimitStatement, self).__init__()
        self.n = n
    def result(self):
        """
        Construye la expresion
        """ 
        return "LIMIT %s" % (self.n)

class SkipStatement(object):
    """
    Crea la sentencia SKIP (similar a OFFSET)
    """ 
    def __init__(self, n):
        super(SkipStatement, self).__init__()
        self.n = n
    def result(self):
        """
        Construye la expresion
        """ 
        return "SKIP %s" % (self.n)

class FetchPlanStatement(object):
    """
    Crea la sentencia FETCHPLAN, usada en OrientDB para definir la estrategia de obtención de recursos.
    """ 
    def __init__(self, direction='*', depth=-1):
        super(FetchPlanStatement, self).__init__()
        self.direction = direction
        self.depth = depth

    def result(self):
        """
        Construye la expresion
        """ 
        return "FETCHPLAN %s:%d" % (self.direction, self.depth)
