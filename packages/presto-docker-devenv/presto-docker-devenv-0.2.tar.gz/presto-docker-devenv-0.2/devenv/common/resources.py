from os import path

_ROOT = path.join(path.abspath(path.dirname(__file__)), '..', '..')


def resources_path():
    return __path_safe(_ROOT, 'images')


def image_path(image):
    return __path_safe(_ROOT, 'images', image)


def __path_safe(*parts):
    resource = path.join(*parts)
    if not path.exists(resource):
        raise Exception('Resource path does not exists: %s' % resource)
    return resource
