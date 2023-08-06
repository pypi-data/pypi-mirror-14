# from . import result
from . import exceptions
from graph_db.types import List
import uuid

class Node(object):
    def __init__(self, data={}):
        self.raw = data
        self.uuid = self.raw.get('uuid')
        self.suid = self.raw.get('suid')
        self.data = self.raw.get('data')
        if not self.data:
            self.data = {}
        self.type = self.raw.get('class', 'V')

    def set(self, key, value):
        self.data[key] = value
        return self

    def get(self, key = None):
        return self.data if key is None else self.data[key]

    def save(self):
        self.driver.Edge.update(self.type, {'uuid': self.uuid}, {
            'data': self.data
        })
        return self
    
    def __str__(self):
        return "Vertex(%s)#%s <%s>" % (self.type, self.suid, self.data)

    @classmethod
    def find(cls, criteria = None, **kwargs):
        criteria = kwargs.get('criteria', {}) if criteria is None else criteria
        criteria.update({'type': 'vertex'})

        try:
            data = cls.driver.Edge.find('V', criteria)[0]
        except IndexError: # 0 results
            # raise exceptions.FetchError('Vertex not found')
            print (":: Vertex not found, using null data :: ")
            data = {}
        inst = cls(data)
        return inst

    """
    Representa un Nodo del grafo
    """
    def __edge(self, edge):
        """
        Este helper generaliza la obtención de lados, si el lado obtenido
        es una cadena (o lista de cadenas) es buscado por el driver, sino
        se pasa directamente a result.Link
        """

        if len(edge) == 1:
            edge = edge[0] 

        if isinstance(edge, list):
            print ("@todo lista de otros (diccionarios)")
            # return Link(edge)
        elif isinstance(edge, str):
            print ("@todo buscar por @RID")
            Link.driver = self.driver
            return Link.find({'@rid': edge })
        elif isinstance(edge, dict):
            print ("@todo buscar por diccionarios")
            # return Link(edge)
        else:
            raise Exception('poor typing')

    def in_(self, label = ''):
        """
        Devuelve los lados que entran hacia el Nodo.
        """
        try:
            edge = self.raw['in_'+label]
        except Exception:
            raise exceptions.FetchError('Edge not found')
        return self.__edge(edge)

    def out(self, label = ''):
        """
        Devuelve los lados que salen del Nodo.
        """
        try:
            edge = self.raw['out_'+label]
        except Exception:
            raise exceptions.FetchError('Edge not found')
        return self.__edge(edge)


class Link(object):
    """
    Representa un Lado del grafo
    """

    def __init__(self, data={}):
        self.raw = data
        self.uuid = self.raw.get('uuid')
        self.suid = self.raw.get('suid')
        self.data = self.raw.get('data')
        if not self.data:
            self.data = {}
        self.type = self.raw.get('class', 'E')

    def set(self, key, value):
        self.data[key] = value
        return self

    def get(self, key = None):
        return self.data if key is None else self.data[key]

    def save(self):
        self.driver.Edge.update(self.type, {'uuid': self.uuid}, {
            'data': self.data
        })
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
        else:
            raise Exception('poor typing')

    def in_(self, *args, **kwargs):
        """
        Devuelve el nodo origen.
        """
        return self.__vertex(self.raw['in'])

    def out(self, *args, **kwargs):
        """
        Devuelve el nodo destino.
        """
        return self.__vertex(self.raw['out'])