from . import exceptions
from graph_db.types import List
import uuid

class Node(object):
    """
    Representa un Nodo del grafo
    """

    def __init__(self, data={}):
        self.raw = data
        self.uuid = self.raw.get('uuid')
        self.suid = self.raw.get('suid')
        self.data = self.raw.get('data')
        if not self.data:
            self.data = {}
        self.type = self.raw.get('class', 'V')

    def __str__(self):
        suid = '-local-' if not self.suid else self.suid
        return "Vertex(%s)#%s <%s>" % (self.type, suid, self.data)

    def __eq__(self, rhs):
        return rhs.uuid == self.uuid
    def __ne__(self, rhs):
        return not(self.__eq__(rhs))

    def set(self, key, value):
        self.data[key] = value
        return self

    def get(self, key = None):
        return self.data if key is None else self.data[key]

    def save(self):
        if self.uuid:
            self.driver.Vertex.update(self.type, {'uuid': self.uuid}, {
                'data': self.data
            })
        else:
            result = self.driver.Vertex.create(self.type, {
                'data': self.data
            })
            self.__init__(result)

        return self
    

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
            return Link(edge)
        elif isinstance(edge, Link):
            return edge
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

    def __str__(self):
        suid = '-local-' if not self.suid else self.suid
        return "Edge(%s)#%s <%s>" % (self.type, suid, self.data)

    def __eq__(self, rhs):
        return rhs.uuid == self.uuid
    def __ne__(self, rhs):
        return not(self.__eq__(rhs))

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
            in_ = self.in_()
            if not in_.suid:
                in_.save()

            out = self.out()
            if not out.suid:
                out.save()
            
            result = self.driver.Edge.create(self.type, out.raw.get('@rid'), in_.raw.get('@rid'), {'data': self.data})
            self.__init__(result)
        return self
    

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
        try:
            if len(vertex) == 1:
                vertex = vertex[0] 
        except TypeError:
            pass

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
            self.raw['out'] = vertex
            return self
        return self.__vertex(self.raw['out'])
    
    def to(self, *args, **kwargs):
        return self.in_(*args, **kwargs)

    def from_(self, *args, **kwargs):
        return self.out(*args, **kwargs)