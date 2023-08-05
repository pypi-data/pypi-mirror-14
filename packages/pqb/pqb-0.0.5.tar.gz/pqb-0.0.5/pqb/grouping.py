#encoding=utf-8
class BaseGrouper(object):
    """
    Clase base para las agrupaciones de clausulas principalmente usado para concatenar expresiones condicionales
    """
    def __init__(self, *args, **kwargs):
        super(BaseGrouper, self).__init__(*args, **kwargs)
        self.items = []
    def append(self, item):
        self.items.append(item)
    def size(self):
        return len(self.items)
    def result(self, concatenator = ' '):
        concatenator = str(concatenator)
        chunks = []
        for i in self.items:
            chunks.append(i.result())
        return concatenator.join( chunks )

# class ANDGrouping(BaseGrouper):
#     def __init__(self, *args, **kwargs):
#         super(ANDGrouping, self).__init__(*args, **kwargs)
#     def result(self):
#         return super(ANDGrouping, self).result(' AND ')

# class ORGrouping(BaseGrouper):
#     def __init__(self, *args, **kwargs):
#         super(ORGrouping, self).__init__(*args, **kwargs)
#     def result(self):
#         return super(ORGrouping, self).result(' OR ')
