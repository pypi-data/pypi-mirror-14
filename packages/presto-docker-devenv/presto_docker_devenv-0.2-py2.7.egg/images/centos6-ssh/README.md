# centos6-java8-oracle

Docker image of CentOS 6 with ssh server installed.
You can log there by using private key 

## Build 
Execute the following from the images/centos6-java8-oracle directory

```
$ sudo docker build -t teradatalabs/centos6-ssh .
$ sudo docker run --rm -it teradatalabs/centos6-ssh /bin/bash
```
