from .node import Node
from .link import Link
import graph_db

def curryInstance(driver, cls):
    instance = cls()
    instance.driver = driver
    return instance

def Factory(driverName, settings):
    driver = graph_db.Factory(driverName, settings)

    driver['Node'] = curryInstance(driver , Node)
    driver['Link'] = curryInstance(driver, Link)
    
    return driver

__version__ = '0.0.1'