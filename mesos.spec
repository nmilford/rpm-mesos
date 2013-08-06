# To build:
#
# You will need the autoconf and libunwind from http://repo.milford.io and the Oracle JDK.
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# sudo yum -y install python26-devel curl-devel libunwind-devel automake autoconf jdk
#
# wget https://raw.github.com/nmilford/rpm-mesos/master/mesos.spec -O ~/rpmbuild/SPECS/mesos.spec
# wget http://mirror.tcpdiag.net/apache/incubator/mesos/mesos-0.12.0-incubating/mesos-0.12.0-incubating.tar.gz -O ~/rpmbuild/SOURCES/mesos-0.12.0-incubating.tar.gz
# wget https://raw.github.com/nmilford/rpm-mesos/master/mesos -O ~/rpmbuild/SOURCES/mesos
# wget https://raw.github.com/nmilford/rpm-mesos/master/mesos.nofiles.conf -O ~/rpmbuild/SOURCES/mesos.nofiles.conf
# wget https://raw.github.com/nmilford/rpm-mesos/master/mesos.conf -O ~/rpmbuild/SOURCES/mesos.conf
# wget https://raw.github.com/nmilford/rpm-mesos/master/mesos-master -O ~/rpmbuild/SOURCES/mesos-master
# wget https://raw.github.com/nmilford/rpm-mesos/master/mesos-slave -O ~/rpmbuild/SOURCES/mesos-slave
#
# QA_RPATHS=$[ 0x0002|0x0001 ] rpmbuild -bb ~/rpmbuild/SPECS/mesos.spec

%define mesos_etc    %{_sysconfdir}/%{name}
%define mesos_config %{mesos_etc}/conf
%define mesos_user   mesos
%define mesos_group  mesos

Name:      mesos
Version:   0.12.0
Release:   1
Summary:   Apache Mesos Cluster Manager
License:   Apache 2.0
URL:       http://mesos.apache.org/
Group:     Applications/System
Source0:   http://mirror.tcpdiag.net/apache/incubator/mesos/%{name}-%{version}-incubating/%{name}-%{version}-incubating.tar.gz
Source1:   mesos
Source2:   mesos-master
Source3:   mesos-slave
Source4:   mesos.nofiles.conf
Source5:   mesos.conf
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Packager:  Nathan Milford <nathan@milford.io>
BuildRequires: python26-devel
BuildRequires: curl-devel
BuildRequires: libunwind-devel
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: jdk
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Requires: jdk
Requires: libunwind
AutoReq: no

%description
Apache Mesos is a cluster manager that provides efficient resource isolation and
sharing across distributed applications, or frameworks. It can run Hadoop, MPI,
Hypertable, Spark, and other applications on a dynamically shared pool of nodes.

%package master
Summary: Apache Mesos Master
Group: Applications/System
Requires: mesos

%description master
Provides the Apache Mesos master daemon, default configuration files, and init scripts.

%package slave
Summary: slave
Group: Applications/System
Requires: mesos

%description slave
Provides the Apache Mesos slave daemon, default configuration files, and init scripts.

%prep

%setup -n %{name}-%{version}
%build
./configure --prefix=%{_prefix} --libdir=%{_libdir}
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR="%{buildroot}"

install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/mesos-master       %{buildroot}/%{_initrddir}/mesos-master
install    -m 755 %_sourcedir/mesos-slave        %{buildroot}/%{_initrddir}/mesos-slave

install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig
install    -m 644 %_sourcedir/mesos              %{buildroot}/%{_sysconfdir}/sysconfig/mesos

install -d -m 755 %{buildroot}/%{_sysconfdir}/security/limits.d/
install    -m 644 %_sourcedir/mesos.nofiles.conf %{buildroot}/%{_sysconfdir}/security/limits.d/mesos.nofiles.conf

install -d -m 755 %{buildroot}/%{mesos_config}
install    -m 644 %_sourcedir/mesos.conf                                         %{buildroot}/%{mesos_config}
install    -m 644 %{buildroot}/usr/var/mesos/conf/mesos.conf.template            %{buildroot}/%{mesos_config}
install    -m 644 %{buildroot}/usr/var/mesos/deploy/mesos-deploy-env.sh.template %{buildroot}/%{mesos_config}
rm -rf %{buildroot}/usr/var/mesos*

install -d -m 755 %{buildroot}/var/log/%{name}

%pre
getent group %{mesos_group} >/dev/null || groupadd -r %{mesos_group}
getent passwd %{mesos_user} >/dev/null || /usr/sbin/useradd --comment "Mesos Daemon User" --shell /bin/bash -M -r -g %{mesos_group} --home %{_datadir}/mesos/ %{mesos_user}

%define service_macro() \
%post %1 \
chkconfig --add %{name}-%1 \
\
%preun %1 \
if [ $1 = 0 ]; then \
  service %{name}-%1 stop > /dev/null 2>&1 \
  chkconfig --del %{name}-%1 \
fi

%service_macro master
%service_macro slave

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/mesos-*
%{_includedir}/mesos/*
%{_libdir}/libmesos*
%{_libexecdir}/mesos/*
%{_sbindir}/*
%{_datadir}/mesos/*

%files master
%defattr(-,root,root,-)
%{_initrddir}/mesos-master
%attr(0755,mesos,mesos) %dir %{_localstatedir}/log/mesos
%config(noreplace) %{mesos_config}/*
%{_sbindir}/mesos-master
%{_sbindir}/*.sh
%{_sysconfdir}/security/*
%{_sysconfdir}/sysconfig/mesos

%files slave
%defattr(-,root,root,-)
%{_initrddir}/mesos-slave
%attr(0755,mesos,mesos) %dir %{_localstatedir}/log/mesos
%config(noreplace) %{mesos_config}/*
%{_sbindir}/mesos-slave
%{_sysconfdir}/security/*
%{_sysconfdir}/sysconfig/mesos

%changelog
* Sat Aug 03 2013 Nathan Milford <nathan@milford.io> 0.12.0-1
- Mesos Mesos Mesos.
