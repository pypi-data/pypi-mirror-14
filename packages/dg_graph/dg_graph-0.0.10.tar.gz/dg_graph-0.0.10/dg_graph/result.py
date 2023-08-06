from graph_db import types

class ResultSet(types.ResultSet):
    """
    Lista de resultados (nodos, lados) generados por una consulta a dg_graph.
    """
    def __init__(self, resultset):
        super(ResultSet, self).__init__(resultset)
        # esta línea cambiará, lo que hace es extraer del resultset
        # el driver que está siendo usado actualmente.
        self.driver = resultset.driver

        # para cada elemento provisto, determinamos que tipo es
        # y luego delegamos a la clase resultado correspondiente.

        for i, target in enumerate(self):
            if target.get('type') == 'vertex':
                self[i] = Node(target)
            elif target.get('type') == 'edge':
                self[i] = Link(target)
            else:
                raise Exception('unknown type: %s' % target)

            # por ultimo, inyectamos el driver actual
            self[i].driver = self.driver

    def in_(self, label = ''):
        """
        Fachada para `in`.
        Si es un conjunto de vértices, Busca los lados que entran un 
        vértice, sino, busca el vértice de donde se origina el lado.
        """
        newList = types.List()
        for i, target in enumerate(self):
            newList.append(target.in_(label))
        newList = newList.flatten()
        newList.driver = self.driver
        return ResultSet(newList)

    def out(self, label = ''):
        """
        Fachada para `out`.
        Si es un conjunto de vértices, Busca los lados que salen un
        vértice, sino, busca el vértice hacia donde se dirige el lado.
        """
        newList = types.List()
        for i, target in enumerate(self):
            newList.append(target.out(label))
        newList = newList.flatten()
        newList.driver = self.driver
        return ResultSet(newList)

class Node():
    def __init__(self, data={}):
        self.data = data

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data[key]

    def save():
        pass

    def find():
        return self.driver.Edge.find('E', self.data)

    """
    Representa un Nodo del grafo
    """
    def __edge(self, edge):
        """
        Este helper generaliza la obtención de lados, si el lado obtenido
        es una cadena (o lista de cadenas) es buscado por el driver, sino
        se pasa directamente a result.Link
        """
        if isinstance(edge, list):
            if isinstance(edge[0], str):
                return self.driver.Edge.find('E', {'@rid': ('IN', edge) })
            else:
                return node.Edge(edge)
        elif isinstance(edge, str):
            return self.driver.Edge.find('E', {'@rid': edge })
        elif isinstance(edge, dict):
            return Edge(edge)
        else:
            raise Exception('poor typing')

    def in_(self, label = ''):
        """
        Devuelve los lados que entran hacia el Nodo.
        """
        edge = self['in_'+label]
        return self.__edge(edge)

    def out(self, label = ''):
        """
        Devuelve los lados que salen del Nodo.
        """
        edge = self['out_'+label]
        return self.__edge(edge)


class Link(types.Result):
    """
    Representa un Lado del grafo
    """
    def __vertex(self, vertex):
        """
        Este helper generaliza la obtención de vértices, si el vértice obtenido
        es una cadena (o lista de cadenas) es buscado por el driver, sino
        se pasa directamente a result.Node
        """
        if isinstance(vertex, list):
            if isinstance(vertex[0], str):
                return self.driver.Node.find('V', {'@rid': ('IN', vertex) })
            else:
                return node.Node(vertex)
        elif isinstance(vertex, str):
            return self.driver.Node.find('V', {'@rid': vertex })
        elif isinstance(vertex, dict):
            return Node(vertex)
        else:
            raise Exception('poor typing')

    def in_(self, *args, **kwargs):
        """
        Devuelve el nodo origen.
        """
        return self.__vertex(self['in'])

    def out(self, *args, **kwargs):
        """
        Devuelve el nodo destino.
        """
        return self.__vertex(self['out'])
