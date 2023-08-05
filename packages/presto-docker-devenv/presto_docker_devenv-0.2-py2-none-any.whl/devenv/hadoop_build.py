#! /usr/bin/env python

from common.resources import image_path
from common.cluster import docker_image_build, docker_image_built
from common.cluster_config import CONTAINER_HADOOP


def run(args):
    if not docker_image_built(CONTAINER_HADOOP.image):
        docker_image_build(image_path('centos6-java8-oracle'))
        docker_image_build(image_path('cdh5-base'))
        docker_image_build(image_path('cdh5-hive'))
