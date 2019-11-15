# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SisCad class from file SisCad.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .unit import SisCad
    return SisCad(iface)
