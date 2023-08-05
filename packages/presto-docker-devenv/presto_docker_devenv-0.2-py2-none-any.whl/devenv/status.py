from __future__ import print_function

import argparse
import httplib
import json
import sys
from socket import error as socket_error

from common.cluster_config import PRESTO_CONTAINERS
from common.cluster_config import CONTAINER_HADOOP
from common import cluster
from common.timeout import timeout

HADOOP_CONTAINER_NAME = CONTAINER_HADOOP.container_name
WAIT = False
LOGGER = print


def print_dash_line():
    LOGGER("-----------------------------------------")


def print_status_header(name):
    print_dash_line()
    LOGGER("          %s" % name)
    print_dash_line()


def docker_status_report():
    print_status_header("docker")
    try:
        cluster.DOCKER.version()
        status = True
    except:
        status = False

    LOGGER("Docker service active: %s" % status)
    LOGGER("Docker host ip: %s" % cluster.DOCKER_HOST)

    return status


def container_exists_status_report(container_name):
    container_exists = cluster.exists(container_name)
    LOGGER("Container exists: %s" % container_exists)
    return container_exists


def container_running_status_report(container_name):
    container_running = cluster.is_running(container_name)
    LOGGER("Container running: %s" % container_running)
    return container_running


def zookeeper_status_report():
    zookeeper_active = cluster.execute(HADOOP_CONTAINER_NAME, "zookeeper-client -cmd ls /")
    LOGGER("Zookeeper active: %s" % zookeeper_active)
    return zookeeper_active


def yarn_status_report():
    yarn_active = cluster.execute(HADOOP_CONTAINER_NAME, "yarn node -list")
    LOGGER("YARN active: %s" % yarn_active)
    return yarn_active


def hive_status_report():
    hive_active = cluster.execute(HADOOP_CONTAINER_NAME, "hive -e 'SHOW TABLES'")
    LOGGER("Hive active: %s" % hive_active)
    return hive_active


def hdfs_status_report():
    try:
        connection = httplib.HTTPConnection(cluster.DOCKER_HOST, 50070)
        connection.request("GET", "/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus")

        response = connection.getresponse()
        if response.status != 200:
            LOGGER("WebHDFS: service not running")
            LOGGER("Health check status != 200: %s" % response.status)
            return False

        response_data = json.load(response)
        state = 'not active (check http://%s:%s/ for details)' % (cluster.DOCKER_HOST, 50070)
        if isinstance(response_data['beans'], list) and len(response_data['beans']) > 0:
            state = response_data['beans'][0]['State']

        hdfs_active = state == "active"
        LOGGER("WebHDFS active: %s" % hdfs_active)
        return hdfs_active
    except socket_error as e:
        LOGGER("WebHDFS: Service connection error")
        LOGGER(e.message)
        LOGGER(False)
    finally:
        connection.close()


def hadoop_status_report():
    print_status_header(HADOOP_CONTAINER_NAME)

    container_exists = container_exists_status_report(HADOOP_CONTAINER_NAME)
    if not container_exists:
        return False

    container_running = container_running_status_report(HADOOP_CONTAINER_NAME)
    if not container_running:
        return False

    return all([
        hdfs_status_report(),
        yarn_status_report(),
        hive_status_report(),
        zookeeper_status_report()])


def presto_status_report(container):
    print_status_header(container.container_name)

    container_exists = container_exists_status_report(container.container_name)
    if not container_exists:
        return False

    container_running = container_running_status_report(container.container_name)
    if not container_running:
        return False

    try:
        connection = httplib.HTTPConnection(cluster.DOCKER_HOST, 8080)
        connection.request("GET", "")
        response = connection.getresponse()
        if response.status != 200:
            LOGGER("Presto: service not running")
            LOGGER("Health check status != 200: %s" % response.status)
            return False

        LOGGER("Presto service active: True")
        return True
    except socket_error:
        LOGGER("Presto: Service connection error)")
        return False
    finally:
        connection.close()


def check_services():
    all_services_running = True

    all_services_running &= docker_status_report()
    all_services_running &= hadoop_status_report()

    for c in PRESTO_CONTAINERS.values():
        all_services_running &= presto_status_report(c)

    print_dash_line()
    LOGGER("All services running: %s" % all_services_running)
    return all_services_running


def parse_args(args):
    global WAIT
    parser = argparse.ArgumentParser(prog="presto-devenv status ")
    parser.add_argument('--wait',
                        help='wait until cluster become ready (with timeout 5 min)',
                        dest='wait',
                        action='store_true')

    args = parser.parse_args(args)
    WAIT = args.wait


def run(args):
    parse_args(args)
    if WAIT:
        global LOGGER
        LOGGER = lambda msg: None
        with timeout(300):
            while not check_services():
                pass
            services_running = True
    else:
        services_running = check_services()
    if services_running:
        sys.exit(0)
    sys.exit(1)
