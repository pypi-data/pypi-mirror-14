from .node import Node
from . import exceptions
from graph_db.types import List
import uuid

class Link(object):
    """
    Representa un Lado del grafo
    """

    def __init__(self, data={}, from_=None, to=None):
        self.raw = data
        self.uuid = self.raw.get('uuid')
        self.suid = self.raw.get('suid')
        self.data = self.raw.get('data')
        if not self.data:
            self.data = {}
        self.type = self.raw.get('class', 'E')
        self.raw['in'] = self.raw.get('in', to)
        self.raw['out'] = self.raw.get('out', from_)

    def set(self, key, value):
        self.data[key] = value
        return self

    def get(self, key = None):
        return self.data if key is None else self.data[key]

    def save(self):
        if self.uuid:
            self.driver.Edge.update(self.type, {'uuid': self.uuid}, {
                'data': self.data
            })
        else:
            #TODO implementarlos con UUID en vez de @rid
            self.in_().save().get('@rid')
            self.out().save().get('@rid')
        return self
    
    def __str__(self):
        return "Edge(%s)#%s <%s>" % (self.type, self.suid, self.data)

    @classmethod
    def find(cls, criteria = None, **kwargs):
        criteria = kwargs.get('criteria', {}) if criteria is None else criteria
        criteria.update({'type': 'edge'})

        try:
            data = cls.driver.Edge.find('E', criteria)[0]
        except IndexError: # 0 results
            # raise exceptions.FetchError('Vertex not found')
            print (":: Edge not found, using null data :: ")
            data = {}
        inst = cls(data)
        return inst

    def __vertex(self, vertex):
        """
        Este helper generaliza la obtención de vértices, si el vértice obtenido
        es una cadena (o lista de cadenas) es buscado por el driver, sino
        se pasa directamente a result.Node
        """
        if len(vertex) == 1:
            vertex = vertex[0] 

        if isinstance(vertex, list):
            print ("@todo lista de otros (diccionarios)")
            # return Link(edge)
        elif isinstance(vertex, str):
            Node.driver = self.driver
            return Node.find({'@rid': vertex })
        elif isinstance(vertex, dict):
            return Node(vertex)
        elif isinstance(vertex, Node):
            return vertex
        else:
            raise Exception('poor typing')

    def in_(self, vertex = None):
        """
        Devuelve el nodo origen.
        """
        if vertex:
            self.raw['in'] = vertex
            return self
        return self.__vertex(self.raw['in'])

    def out(self, vertex = None):
        """
        Devuelve el nodo destino.
        """
        if vertex:
            self.raw['in'] = vertex
            return self
        return self.__vertex(self.raw['out'])