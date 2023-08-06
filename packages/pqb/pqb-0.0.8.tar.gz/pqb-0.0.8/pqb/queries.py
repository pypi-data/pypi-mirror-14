#encoding=utf-8
from . import statements
from . import grouping
from . import expressions
import json

class Select:
    """SELECT Query Builder"""
    def __init__(self, *fields):
        """
        Inicializa la consulta SELECT opcionalmente los argumentos pasados serna considerados campos para la proyección.
        """
        super(self.__class__, self).__init__()
        self.raw_fields = fields
        self.raw_fields = []
        self.raw_fields_group = []
        self.fields = []
        self.group_fields = []
        self.raw_tables = []
        self.raw_order_by = []
        self.order_by_fields = []
        self.tables = []
        self.where_criteria = grouping.BaseGrouper()

    def __prepareData__(self):
        """
        Helper para preparar los datos para la produccion del SQL final.
        """
        if isinstance(self.raw_fields, str):
            self.raw_fields = self.raw_fields.split(',')

        for x in self.raw_fields:
            self.fields.append(expressions.AliasExpression(x).result())
        
        if len(self.fields) == 0:
            self.fields.append('*')

        for x in self.raw_tables:
            self.tables.append(expressions.AliasExpression(x).result())

        if isinstance(self.raw_fields_group, str):
            self.raw_fields_group = self.raw_fields_group.split(',')


        for x in self.raw_fields_group:
            self.group_fields.append(expressions.AliasExpression(x).result())


        if isinstance(self.raw_order_by, str):
            self.raw_order_by = self.raw_order_by.split(',')

        for x in self.raw_order_by:
            self.order_by_fields.append(expressions.OrderByExpression(*x).result())

    def from_(self, table, alias=None):
        """
        Establece el origen de datos (y un alias opcionalmente).
        """
        if isinstance(table, str):
            table = [[table, alias]]
        self.raw_tables = table
        return self

    def where(self, field, value = None, operator = None):
        """
        Establece condiciones para la consulta unidas por AND
        """
        if field is None:
            return self
        conjunction = None
        if value is None and isinstance(field, dict):
            for f,vo in field.items():
                if self.where_criteria.size() > 0:
                    conjunction = 'AND'
                try:
                    operator, v = vo
                except Exception as e:
                    v = vo
                    operator = None
                self.where_criteria.append(expressions.ConditionExpression(f, v, operator=operator, conjunction=conjunction))
                
        else:
            if self.where_criteria.size() > 0:
                    conjunction = 'AND'
            self.where_criteria.append(expressions.ConditionExpression(field, value, operator=operator, conjunction=conjunction))
        return self

    def where_or(self, field, value = None, operator = None):
        """
        Establece condiciones para la consulta unidas por OR
        """
        if field is None:
            return self
        conjunction = None
        if value is None and isinstance(field, dict):
            for f,v in field.items():
                if self.where_criteria.size() > 0:
                    conjunction = 'OR'

                self.where_criteria.append(expressions.ConditionExpression(f, v, operator=operator, conjunction=conjunction))
                
        else:
            if self.where_criteria.size() > 0:
                    conjunction = 'OR'
            self.where_criteria.append(expressions.ConditionExpression(field, value, operator=operator, conjunction=conjunction))
        return self

    def group_by(self, *args):
        """
        Indica los campos para agrupación
        """
        if len(args) == 1:
            self.raw_fields_group = args[0].split(',')
        else:
            self.raw_fields_group = list(args)
        return self

    def order_by(self, field, orientation='ASC'):
        """
        Indica los campos y el criterio de ordenamiento
        """
        if isinstance(field, list):
            self.raw_order_by.append(field)
        else:
            self.raw_order_by.append([field, orientation])

        return self

    def result(self, *args, **kwargs):
        """
        Construye la consulta SQL
        """
        prettify = kwargs.get('pretty', False)
        self.__prepareData__()
        sql = 'SELECT '
        sql +=  ', '.join(self.fields)
        
        if len(self.tables) > 0:
            if prettify:
                sql += '\n'
            else:
                sql += ' '
            sql +=  'FROM '
            sql +=  ', '.join(self.tables)
        if self.where_criteria.size() > 0:
            if prettify:
                sql += '\n'
            else:
                sql += ' '
            sql +=  'WHERE '
            sql +=  self.where_criteria.result()
        if len(self.group_fields) > 0:
            if prettify:
                sql += '\n'
            else:
                sql += ' '
            sql +=  'GROUP BY '
            sql +=  ', '.join(self.group_fields)
        if len(self.order_by_fields) > 0:
            if prettify:
                sql += '\n'
            else:
                sql += ' '
            sql +=  'ORDER BY '
            sql +=  ', '.join(self.order_by_fields)
            if prettify:
                sql += '\n'
            else:
                sql += ' '

        return sql

class Delete(object):
    """
    DELETE Query Builder
    """

    def __init__(self, type):
        """
        Inicializa la consulta, type = recurso (Vertex|Edge)
        """
        super(Delete, self).__init__()
        self._class = None
        self._cluster = None
        self._type = None
        self.data = {}
        self.where_criteria = grouping.BaseGrouper()
        self._type = type
    
    def class_(self, _class):
        """
        Especifica la clase para eliminar
        """
        self._class = _class
        return self
        
    def where(self, field, value = None, operator = None):
        """
        Establece condiciones para la consulta unidas por AND
        """
        if field is None:
            return self
        conjunction = None
        if value is None and isinstance(field, dict):
            for f,v in field.items():
                if self.where_criteria.size() > 0:
                    conjunction = 'AND'
                self.where_criteria.append(expressions.ConditionExpression(f, v, operator=operator, conjunction=conjunction))
                
        else:
            if self.where_criteria.size() > 0:
                    conjunction = 'AND'
            self.where_criteria.append(expressions.ConditionExpression(field, value, operator=operator, conjunction=conjunction))
        return self

    def where_or(self, field, value = None, operator = None):
        """
        Establece condiciones para la consulta unidas por OR
        """
        if field is None:
            return self
        conjunction = None
        if value is None and isinstance(field, dict):
            for f,v in field.items():
                if self.where_criteria.size() > 0:
                    conjunction = 'OR'
                self.where_criteria.append(expressions.ConditionExpression(f, v, operator=operator, conjunction=conjunction))
                
        else:
            if self.where_criteria.size() > 0:
                    conjunction = 'OR'
            self.where_criteria.append(expressions.ConditionExpression(field, value, operator=operator, conjunction=conjunction))
        return self

    def result(self, *args, **kwargs):
        """
        Construye la consulta SQL
        """
        prettify = kwargs.get('pretty', False)

        sql = 'DELETE %s %s' % (self._type, self._class)
        
        if prettify:
            sql += '\n'
        else:
            sql += ' '

        if self.where_criteria.size() > 0:
            sql +=  'WHERE '
            sql +=  self.where_criteria.result()
            if prettify:
                sql += '\n'
            else:
                sql += ' '
        
        return sql

class Create(object):
    "CREATE query builder"

    def __init__(self, type):
        """
        Inicializa la consulta, type = recurso (Vertex|Edge)
        """
        super(Create, self).__init__()
        self._class = None
        self._cluster = None
        self._type = None
        self._from = None
        self._to = None
        self.data = {}
        self._type = type
    
    def class_(self, _class):
        """
        Especifica la clase para crear
        """
        self._class = _class
        return self
        
    def cluster(self, cluster):
        """
        Especifica el cluster donde se almacenara el nuevo recurso
        """
        self._cluster = cluster
        return self
    
    def from_(self, From):
        """
        [Edge-only] especifica el origen del lado
        """
        if self._type.lower() != 'edge':
            raise ValueError('Cannot set From/To to non-edge objects')
        self._from = From
        return self
    
    def to(self, to):
        """
        [Edge-only] especifica el destino del lado
        """
        if self._type.lower() != 'edge':
            raise ValueError('Cannot set From/To to non-edge objects')
        self._to = to
        return self

    def set(self, field, value = None):
        """
        [Edge|Vertex] establece datos del recurso
        """
        if value is None and isinstance(field, dict):
            self.content(field)
        if field and value:
            self.data[field] = value
        return self

    def content(self, obj):
        """
        [Edge|Vertex] establece datos del recurso
        """
        self.data.update(obj)
        return self

    def result(self, *args, **kwargs):
        """
        Construye la consulta SQL
        """
        prettify = kwargs.get('pretty', False)

        sql = 'CREATE %s %s' % (self._type, self._class)
        
        if prettify:
            sql += '\n'
        else:
            sql += ' '

        if self._type.lower() == 'edge':
            sql += " FROM %s TO %s " % (self._from, self._to)
        
        if self._cluster:
            sql += 'CLUSTER %s' % self._cluster
            if prettify:
                sql += '\n'
            else:
                sql += ' '
        
        if self.data:
            sql += 'CONTENT ' + json.dumps(self.data)
        return sql

class Update(object):
    """
    UPDATE Query Builder
    """
    def __init__(self, _class):
        """
        Inicializa la clase, _class = origen donde actualizar
        """
        super(Update, self).__init__()
        self._class = None
        self._cluster = None
        self.data = {}
        self.where_criteria = grouping.BaseGrouper()
        self._class = _class

    def set(self, field, value = None):
        """
        [Edge|Vertex] establece datos del recurso
        """
        if value is None and isinstance(field, dict):
            self.content(field)
        if field and value:
            self.data[field] = value
        return self

    def content(self, obj):
        """
        [Edge|Vertex] establece datos del recurso
        """
        self.data.update(obj)
        return self

    def where(self, field, value = None, operator = None):
        """
        Establece condiciones para la consulta unidas por AND
        """
        if field is None:
            return self
        conjunction = None
        if value is None and isinstance(field, dict):
            for f,v in field.items():
                if self.where_criteria.size() > 0:
                    conjunction = 'AND'
                self.where_criteria.append(expressions.ConditionExpression(f, v, operator=operator, conjunction=conjunction))
                
        else:
            if self.where_criteria.size() > 0:
                    conjunction = 'AND'
            self.where_criteria.append(expressions.ConditionExpression(field, value, operator=operator, conjunction=conjunction))
        return self

    def where_or(self, field, value = None, operator = None):
        """
        Establece condiciones para la consulta unidas por OR
        """
        if field is None:
            return self
        conjunction = None
        if value is None and isinstance(field, dict):
            for f,v in field.items():
                if self.where_criteria.size() > 0:
                    conjunction = 'OR'
                self.where_criteria.append(expressions.ConditionExpression(f, v, operator=operator, conjunction=conjunction))
                
        else:
            if self.where_criteria.size() > 0:
                    conjunction = 'OR'
            self.where_criteria.append(expressions.ConditionExpression(field, value, operator=operator, conjunction=conjunction))
        return self

    def result(self, *args, **kwargs):
        """
        Construye la consulta SQL
        """
        prettify = kwargs.get('pretty', False)

        sql = 'UPDATE %s' % self._class
        
        if prettify:
            sql += '\n'
        else:
            sql += ' '
        
        if self.data:
            sql += 'MERGE ' + json.dumps(self.data)
            if prettify:
                sql += '\n'
            else:
                sql += ' '

        if self.where_criteria.size() > 0:
            sql +=  'WHERE '
            sql +=  self.where_criteria.result()
            if prettify:
                sql += '\n'
            else:
                sql += ' '
        
        return sql
