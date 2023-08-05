from . import result
from graph_db.types import List

class Node(object):
    def create(self, *args, **kwargs):
        res = self.driver.Vertex.create(*args, **kwargs)
        return result.Node(List(res))
    
    def update(self, *args, **kwargs):
        res = self.driver.Vertex.update(*args, **kwargs)
        return result.Node(List(res))

    def search(self, *args, **kwargs):
        res = self.driver.Vertex.search(*args, **kwargs)
        res.driver = self.driver
        return result.Node(List(res))
    
    def delete(self, *args, **kwargs):
        return self.driver.Vertex.delete(*args, **kwargs)

    def find(self, *args, **kwargs):
        res = self.driver.Vertex.find(*args, **kwargs)
        res.driver = self.driver
        return result.ResultSet(res)

