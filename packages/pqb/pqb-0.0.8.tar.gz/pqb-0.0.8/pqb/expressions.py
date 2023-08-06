#encoding=utf-8
import re
REGEX_CLEANER = re.compile(r"[^a-z0-9_@]", re.I)

class AliasExpression(object):
    """
    Crea una expresion SQL alias <campo> AS <alias> o simplemente <campo> si no fue provisto un alias
    """
    def __init__(self, field_name, alias=None, *args, **kwargs):
        super(self.__class__, self).__init__()
        if isinstance(field_name, list):
            field_name, alias = field_name
        if ' as ' in field_name.lower():
            self.field_name, self.alias = field_name.split(' as ')
        else:
            self.field_name = field_name
            self.alias = alias
    def result(self):
        """
        Construye la expresion
        """ 
        field = re.sub(REGEX_CLEANER, '', self.field_name)

        if self.alias:
            alias = re.sub(REGEX_CLEANER, '', self.alias)
            return "%s AS %s" % (field, alias)
        else:
            return field

class ConditionExpression(object):
    """
    Crea una expresion SQL condicional, usadas en WHERE y HAVING:
    <campo> <operador> <valor>
    """
    def __init__(self, field, value, *args, **kwargs):
        self.field = field
        self.value = value
        self.operator = '=' if kwargs.get('operator') is None else kwargs['operator']
        self.conjunction = kwargs.get('conjunction')

    def result(self):
        """
        Construye la expresion
        """ 
        field = re.sub(REGEX_CLEANER, '', self.field)

        try:
            value = float(self.value)
        except TypeError:
        	value = "(%s)" % ( "', '".join(self.value) )
        except ValueError:
            value = str(self.value) \
                .replace("\\", r"\\") \
                .replace('"', r'\"') \
                .replace("'", r"\'")

            value = "'%s'" % value
        
        res = "%s %s %s" % (field, self.operator, value)

        if self.conjunction:
            res = "%s %s" % (self.conjunction, res)
        
        return res

class OrderByExpression(object):
    """
    Crea una expresion SQL de ordenamiento.
    """ 
    def __init__(self, field, orientation = 'ASC'):
        super(OrderByExpression, self).__init__()

        if isinstance(field, list):
            self.field, self.orientation = field[0:2]
        elif 'ASC' in field.upper() or 'DESC' in field.upper():
            self.field, self.orientation = field.split(' ')
        else:
            self.field = field
            self.orientation = orientation
    def result(self):
        """
        Construye la expresion
        """ 
        return "%s %s" % (self.field, self.orientation)