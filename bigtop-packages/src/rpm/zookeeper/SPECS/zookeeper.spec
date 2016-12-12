# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
%define etc_zookeeper /etc/%{name}
%define bin_zookeeper %{_bindir}
%define lib_zookeeper /usr/lib/%{name}
%define log_zookeeper /var/log/%{name}
%define run_zookeeper /var/run/%{name}
%define vlb_zookeeper /var/lib/%{name}
%define svc_zookeeper %{name}-server
%define svc_zookeeper_rest %{name}-rest
%define man_dir %{_mandir}

%define doc_zookeeper %{_docdir}/%{name}-%{zookeeper_version}
%define alternatives_cmd /usr/sbin/alternatives

Name: zookeeper
Version: %{zookeeper_version}
Release: %{zookeeper_release}
Summary: A high-performance coordination service for distributed applications.
URL: http://zookeeper.apache.org/
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
License: ASL 2.0
Source0: %{name}-%{zookeeper_base_version}.tar.gz
Source1: do-component-build
Source2: install_zookeeper.sh
Source3: zookeeper-server.sh
Source5: zookeeper.1
Source6: zoo.cfg
Source7: zookeeper.default
Source8: init.d.tmpl
Source9: zookeeper-rest.svc
Source10: zookeeper-rest.service
Source11: zookeeper-server.service
Source12: tmpfiles.tmpl
#BIGTOP_PATCH_FILES
BuildRequires: autoconf, automake, cppunit-devel
Requires(pre): coreutils, /usr/sbin/groupadd, /usr/sbin/useradd
Requires: bigtop-utils >= 1.1

%description
ZooKeeper is a centralized service for maintaining configuration information, 
naming, providing distributed synchronization, and providing group services. 
All of these kinds of services are used in some form or another by distributed 
applications. Each time they are implemented there is a lot of work that goes 
into fixing the bugs and race conditions that are inevitable. Because of the 
difficulty of implementing these kinds of services, applications initially 
usually skimp on them ,which make them brittle in the presence of change and 
difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.  

%package server
Summary: The Hadoop Zookeeper server
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires: /lib/lsb/init-functions
%if 0%{?rhel} >= 7
Requires: systemd, systemd-sysv
BuildRequires: systemd
%else
Requires(post): initscripts chkconfig
Requires(preun):  initscripts chkconfig
Requires(postun): initscripts chkconfig
%endif

%description server
This package starts the zookeeper server on startup

%package rest
Summary: ZooKeeper REST Server
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: systemd, systemd-sysv
BuildRequires: systemd
%else
Requires(post): initscripts chkconfig
Requires(preun):  initscripts chkconfig
Requires(postun): initscripts chkconfig
%endif

%package native
Summary: C bindings for ZooKeeper clients
Group: Development/Libraries

%description native
Provides native libraries and development headers for C / C++ ZooKeeper clients. Consists of both single-threaded and multi-threaded implementations.

%description rest
This package starts the zookeeper REST server on startup

%prep
%setup -n %{name}-%{zookeeper_base_version}

#BIGTOP_PATCH_COMMANDS

%build
bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
cp $RPM_SOURCE_DIR/zookeeper.1 $RPM_SOURCE_DIR/zoo.cfg $RPM_SOURCE_DIR/zookeeper.default .
bash %{SOURCE2} \
          --build-dir=build/%{name}-%{zookeeper_base_version} \
          --doc-dir=%{doc_zookeeper} \
          --prefix=$RPM_BUILD_ROOT \
          --system-include-dir=%{_includedir} \
          --system-lib-dir=%{_libdir}


%if 0%{?rhel} >= 7
%__install -d -m 0755 $RPM_BUILD_ROOT/%{lib_zookeeper}/libexec
%__install -d -m 0755 $RPM_BUILD_ROOT/%{_unitdir}
server_init_file=$RPM_BUILD_ROOT/%{lib_zookeeper}/libexec/%{svc_zookeeper}
rest_init_file=$RPM_BUILD_ROOT/%{lib_zookeeper}/libexec/%{svc_zookeeper_rest}
%__cp %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}/%{name}-rest.service
%__cp %{SOURCE11} $RPM_BUILD_ROOT/%{_unitdir}/%{name}-server.service
%__install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/tmpfiles.d
sed "s|__RUN_DIR__|%{run_zookeeper}|;s|__OWNER__|zookeeper|;s|__GROUP__|zookeeper|;s|__PERM__|0755|" %{SOURCE12} > $RPM_BUILD_ROOT/%{_sysconfdir}/tmpfiles.d/%{name}.conf
%else
%__install -d -m 0755 $RPM_BUILD_ROOT/%{_initrddir}
server_init_file=$RPM_BUILD_ROOT/%{_initrddir}/%{svc_zookeeper}
rest_init_file=$RPM_BUILD_ROOT/%{_initrddir}/%{svc_zookeeper_rest}
%endif
%__cp %{SOURCE3} $server_init_file
bash $RPM_SOURCE_DIR/init.d.tmpl $RPM_SOURCE_DIR/zookeeper-rest.svc rpm $rest_init_file
chmod 755 $server_init_file
chmod 755 $rest_init_file

%pre
getent group zookeeper >/dev/null || groupadd -r zookeeper
getent passwd zookeeper > /dev/null || useradd -c "ZooKeeper" -s /sbin/nologin -g zookeeper -r -d %{vlb_zookeeper} zookeeper 2> /dev/null || :

%__install -d -o zookeeper -g zookeeper -m 0755 %{run_zookeeper}
%__install -d -o zookeeper -g zookeeper -m 0755 %{log_zookeeper}

# Manage configuration symlink
%post
%{alternatives_cmd} --install %{etc_zookeeper}/conf %{name}-conf %{etc_zookeeper}/conf.dist 30
%__install -d -o zookeeper -g zookeeper -m 0755 %{vlb_zookeeper}
%if 0%{?rhel} >= 7
systemd-tmpfiles --create %{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif

%preun
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{name}-conf %{etc_zookeeper}/conf.dist || :
fi

%post server
%if 0%{?rhel} >= 7
  systemctl daemon-reload
%else
	chkconfig --add %{svc_zookeeper}
%endif

%preun server
if [ $1 = 0 ] ; then
%if 0%{?rhel} >= 7
  systemctl disable --no-reload %{name}-server > /dev/null 2>&1 || :
  systemctl stop %{name}-server > /dev/null 2>&1 || :
%else
	service %{svc_zookeeper} stop > /dev/null 2>&1
	chkconfig --del %{svc_zookeeper}
%endif
fi

%postun server
if [ $1 -ge 1 ]; then
%if 0%{?rhel} >= 7
  systemctl try-restart %{name}-%1 >/dev/null 2>&1 || :
%else
  service %{svc_zookeeper} condrestart > /dev/null 2>&1
%endif
fi

%post rest
%if 0%{?rhel} >= 7
  systemctl daemon-reload
%else
	chkconfig --add %{svc_zookeeper_rest}
%endif

%preun rest
if [ $1 = 0 ] ; then
%if 0%{?rhel} >= 7
  systemctl disable --no-reload %{name}-rest > /dev/null 2>&1 || :
  systemctl stop %{name}-rest > /dev/null 2>&1 || :
%else
	service %{svc_zookeeper_rest} stop > /dev/null 2>&1
	chkconfig --del %{svc_zookeeper_rest}
%endif
fi

%postun rest
if [ $1 -ge 1 ]; then
%if 0%{?rhel} >= 7
  systemctl try-restart %{name}-rest >/dev/null 2>&1 || :
%else
  service %{svc_zookeeper_rest} condrestart > /dev/null 2>&1
%endif
fi

#######################
#### FILES SECTION ####
#######################
%files
%defattr(-,root,root)
%config(noreplace) %{etc_zookeeper}/conf.dist
%config(noreplace) /etc/default/zookeeper
%if 0%{?rhel} >= 7
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif
%{lib_zookeeper}
%{bin_zookeeper}/zookeeper-server
%{bin_zookeeper}/zookeeper-server-initialize
%{bin_zookeeper}/zookeeper-client
%{bin_zookeeper}/zookeeper-server-cleanup
%doc %{doc_zookeeper}
%{man_dir}/man1/zookeeper.1.*

%files server
%if 0%{?rhel} >= 7
%attr(0644,root,root)%{_unitdir}/%{name}-server.service
%attr(0755,root,root) %{lib_zookeeper}/libexec/%{svc_zookeeper}
%else
%attr(0755,root,root) %{_initrddir}/%{svc_zookeeper}
%endif

%files rest
%if 0%{?rhel} >= 7
%attr(0644,root,root)%{_unitdir}/%{name}-rest.service
%attr(0755,root,root) %{lib_zookeeper}/libexec/%{svc_zookeeper_rest}
%else
%attr(0755,root,root) %{_initrddir}/%{svc_zookeeper_rest}
%endif

%files native
%defattr(-,root,root)
%{lib_zookeeper}-native
%{bin_zookeeper}/cli_*
%{bin_zookeeper}/load_gen*
%{_includedir}/zookeeper
%{_libdir}/*

