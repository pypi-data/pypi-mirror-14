"""
dg_graph

[diggi] Traverso de Grafos
"""

from .node import Node
from .link import Link
import graph_db

def curryInstance(driver, cls):
    """
    @todo generalizar este helper
    Este helper inyecta propiedades dentro de instancias de clases
    útil para garantizar la existencia de propiedades
    pero no forzarlas en el constructor.
    """

    instance = cls()
    instance.driver = driver
    return instance

def Factory(driverName, settings):
    """Factory(name, settings) -> DriverPackage

    Genera las instancias de Node y Link en el driver generado
    por GraphDB.
    """

    driver = graph_db.Factory(driverName, settings)
    
    driver['Node'] = Node
    driver['Link'] = Link
    
    Node.driver = Link.driver = driver

    return driver

__version__ = '0.0.4'