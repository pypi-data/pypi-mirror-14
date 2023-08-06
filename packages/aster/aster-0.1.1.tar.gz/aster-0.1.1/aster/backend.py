import aster.g as g


def import_backend():
    module_name = 'aster.backends.{0}'.format(g.config['backend']['name'])
    m = __import__(module_name)
    for attr in module_name.split('.')[1:]:
        m = getattr(m, attr)

    return m
