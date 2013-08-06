rpm-mesos
=========

An RPM spec file build and install the Apache Mesos Cluster Manager.

To build:

You will need the autoconf and libunwind from http://repo.milford.io and the Oracle JDK.

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`sudo yum -y install python26-devel curl-devel libunwind-devel automake autoconf jdk`

`wget https://raw.github.com/nmilford/rpm-mesos/master/mesos.spec -O ~/rpmbuild/SPECS/mesos.spec`

`wget http://mirror.tcpdiag.net/apache/incubator/mesos/mesos-0.12.0-incubating/mesos-0.12.0-incubating.tar.gz -O ~/rpmbuild/SOURCES/mesos-0.12.0-incubating.tar.gz`

`wget https://raw.github.com/nmilford/rpm-mesos/master/mesos -O ~/rpmbuild/SOURCES/mesos`

`wget https://raw.github.com/nmilford/rpm-mesos/master/mesos.nofiles.conf -O ~/rpmbuild/SOURCES/mesos.nofiles.conf`

`wget https://raw.github.com/nmilford/rpm-mesos/master/mesos.conf -O ~/rpmbuild/SOURCES/mesos.conf`

`wget https://raw.github.com/nmilford/rpm-mesos/master/mesos-master -O ~/rpmbuild/SOURCES/mesos-master`

`wget https://raw.github.com/nmilford/rpm-mesos/master/mesos-slave -O ~/rpmbuild/SOURCES/mesos-slave`

`QA_RPATHS=$[ 0x0002|0x0001 ]rpmbuild -bb ~/rpmbuild/SPECS/mesos.spec`
