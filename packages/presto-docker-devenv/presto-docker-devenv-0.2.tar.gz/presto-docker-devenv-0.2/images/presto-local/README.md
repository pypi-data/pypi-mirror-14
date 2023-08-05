# presto local

To build docker image for local presto source code use ```presto-devenv presto build-image``` command.
You need to pass three parameters:

```
  --presto-source PRESTO_SOURCE_ROOT
                        Presto source directory
  --master-config PRESTO_MASTER_CONFIG_DIR
                        Configuration directory to be used within image for
                        master node
  --worker-config PRESTO_WORKER_CONFIG_DIR
                        Configuration directory to be used within image worker
                        node
```

Example execution (script internally uses sudo):

```
$ presto-devenv presto build-image \
  --presto-source /home/sogorkis/repos/presto/ \
  --master-config example_configs/master/ \
  --worker-config example_configs/worker/
```

Example execution without rebuilding presto:

```
$ presto-devenv presto build-image \
  --presto-source /home/sogorkis/repos/presto/ \
  --master-config example_configs/master/ \
  --worker-config example_configs/worker/ \
  --no-build
```

Verify docker image was built:

```
$ sudo docker images | grep presto-dev-env
teradatalabs/presto-dev-env         latest                                                          dfd979479b35        4 seconds ago       1.142 GB
teradatalabs/presto-dev-env         d4c65f5d6a41bb204e99632d2d52c6bdb19371e4-2015-04-09T14-06-13Z   dfd979479b35        4 seconds ago       1.142 GB
```
