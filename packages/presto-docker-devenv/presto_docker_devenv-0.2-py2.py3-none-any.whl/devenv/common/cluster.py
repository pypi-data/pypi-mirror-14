import os
import time
import logging
from urlparse import urlparse

from cluster_config import IMAGES_GROUP
from docker.client import Client
from docker.utils import kwargs_from_env
from docker.errors import NotFound
from resources import resources_path
from vagrant import Vagrant, make_file_cm
from .. import LOG_FILE

DEVNULL = open(os.devnull, 'w')


def __init_docker():
    kwargs = kwargs_from_env()

    if 'tls' in kwargs:
        # see http://docker-py.readthedocs.org/en/latest/boot2docker/
        import requests.packages.urllib3 as urllib3

        urllib3.disable_warnings()
        kwargs['tls'].assert_hostname = False

    host = "localhost"
    if 'base_url' in kwargs:
        host = urlparse(kwargs['base_url']).hostname

    docker = Client(**kwargs)
    try:
        docker.version()
    except:
        raise Exception("Please set up 'docker' correctly")
    return (docker, host)


def __init_vagrant():
    vagrant_env = os.environ.copy()
    vagrant_env["VAGRANT_DOTFILE_PATH"] = "~/.presto-devenv"
    log_cm = make_file_cm('/tmp/presto-devenv.log')
    return Vagrant(env=vagrant_env, root=resources_path(), out_cm=log_cm, err_cm=log_cm)


(DOCKER, DOCKER_HOST) = __init_docker()
VAGRANT = __init_vagrant()


def exists(container_name):
    return _status(container_name) != 'not_created'


def _status(container_name):
    status = VAGRANT.status(vm_name=container_name)
    if len(status) != 1:
        raise Exception("Unable to get status for %s" % container_name)
    return status[0].state


def is_running(container_name):
    return _status(container_name) == 'running'


def clean(container_name):
    VAGRANT.destroy(vm_name=container_name)


def start(container_name):
    VAGRANT.up(vm_name=container_name)


def stop(container_name):
    VAGRANT.halt(vm_name=container_name)


def execute(container_name, command):
    # TODO support boot2docker
    id = DOCKER.exec_create(container=container_name, cmd=command, stdout=False, stderr=False)['Id']
    DOCKER.exec_start(id)
    while True:
        exit_code = DOCKER.exec_inspect(id)['ExitCode']
        if exit_code is not None:
            return exit_code == 0
        time.sleep(1)


def docker_image_build(path, tag=None):
    if tag is None:
        tag = '%s/%s' % (IMAGES_GROUP, os.path.basename(path))
    print 'Building docker image %s' % tag
    output = DOCKER.build(path=path, tag=tag)
    logging.info("Building docker image %s, %s" % (path, tag))
    for line in output:
        logging.debug(line)
        success = 'error' not in line
    if not success:
        raise Exception("%s was not built successfully consult log file %s for more details" % (tag, LOG_FILE))


def docker_image_built(image):
    try:
        DOCKER.inspect_image(image)
        return True
    except NotFound:
        return False


def docker_tag(image, tag):
    raise Exception('docker_tag is not yet supported')
