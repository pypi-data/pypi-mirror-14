from graph_db import types

class ResultSet(types.ResultSet):
    def __init__(self, resultset):
        super(ResultSet, self).__init__(resultset)
        self.driver = resultset.driver
        for i, target in enumerate(self):
            if target.get('type') == 'vertex':
                self[i] = Node(target)
            elif target.get('type') == 'edge':
                self[i] = Link(target)
            else:
                raise Exception('unknown type: %s' % target)

            self[i].driver = self.driver

    def in_(self, label = ''):
        newList = types.List()
        for i, target in enumerate(self):
            newList.append(target.in_(label))
        newList = newList.flatten()
        newList.driver = self.driver
        return ResultSet(newList)

    def out(self, label = ''):
        newList = types.List()
        for i, target in enumerate(self):
            newList.append(target.out(label))
        newList = newList.flatten()
        newList.driver = self.driver
        return ResultSet(newList)

class Node(types.Result):
    def __edge(self, edge):
        if isinstance(edge, list):
            if isinstance(edge[0], str):
                return self.driver.Link.find('E', {'@rid': ('IN', edge)})
            else:
                return link.Link(edge)
        else:
            return link.Link(edge)

    def in_(self, label = ''):
        edge = self['in_'+label]
        return self.__edge(edge)

    def out(self, label = ''):
        edge = self['out_'+label]
        return self.__edge(edge)


class Link(types.Result):
    def __vertex(self, vertex):
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
        return self.__vertex(self['in'])

    def out(self, *args, **kwargs):
        return self.__vertex(self['out'])


