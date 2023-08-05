from . import result
from graph_db.types import List

class Link(object):
    def create(self, *args, **kwargs):
        res = self.driver.Edge.create(*args, **kwargs)
        return result.Link(List(res))
    
    def update(self, *args, **kwargs):
        res = self.driver.Edge.update(*args, **kwargs)
        return result.Link(List(res))

    def search(self, *args, **kwargs):
        res = self.driver.Edge.search(*args, **kwargs)
        return result.Link(List(res))
    
    def delete(self, *args, **kwargs):
        return self.driver.Edge.delete(*args, **kwargs)

    def find(self, *args, **kwargs):
        res = self.driver.Edge.find(*args, **kwargs)
        res.driver = self.driver
        return result.ResultSet(res)

