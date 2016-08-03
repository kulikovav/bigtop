#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define knox_name knox
%define knox_libdirname /opt

Name: 	 	%{knox_name}
Version:	%{knox_version}
Release:	%{knox_release}
Summary:	Knox is an authenticating reverse proxy and provide a way to provide perimeter security for Hadoop clusters.
License:	Apache License, Version 2.0
URL:		http://knox.apache.org/
Group:		Applications/Server
Buildroot:	%{_topdir}/INSTALL/%{knox_name}-%{knox_version}
BuildArch:	noarch
Source0:	%{knox_name}-%{knox_base_version}.zip
Source1:	do-component-build
Source2:	install_knox.sh
Source3:	bigtop.bom
Source4:	knox.init
Patch0:		patch0.diff
Patch1:		patch1.diff
Requires:	kaosv

%description
The Apache Knox Gateway is a REST API Gateway for interacting with Apache Hadoop clusters.

The Knox Gateway provides a single access point for all REST interactions with Apache Hadoop clusters.

In this capacity, the Knox Gateway is able to provide valuable functionality to aid in the control,
integration, monitoring and automation of critical administrative and analytical needs of the enterprise.

* Authentication (LDAP and Active Directory Authentication Provider)
* Federation/SSO (HTTP Header Based Identity Federation)
* Authorization (Service Level Authorization)
* Auditing

%prep
echo "Knox installation preparation"

%setup -n %{knox_name}-%{knox_base_version}

%patch0 -p1
%patch1 -p1

%build
echo "Knox installation build"
env KNOX_BASE_VERSION=%{knox_base_version} bash %{SOURCE1}

%install
######################
sh -x %{SOURCE2} \
          --build-dir=target \
          --prefix=$RPM_BUILD_ROOT \
          --knox-version=%{knox_base_version} \
          --lib-dir=%{knox_libdirname}

%__install -d -m 0775 ${RPM_BUILD_ROOT}/%{_localstatedir}/lib/knox/data
%__install -d -m 0775 ${RPM_BUILD_ROOT}/%{_localstatedir}/log/knox
%__install -d -m 0775 ${RPM_BUILD_ROOT}/%{_localstatedir}/run/knox
%__install -d -m 0775 ${RPM_BUILD_ROOT}/%{_sysconfdir}/knox/conf
%__install -d -m 0775 ${RPM_BUILD_ROOT}/%{_sysconfdir}/knox/conf.dist
%__install -pDm 755 %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d/%{knox_name}

cp -rp ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/conf/* ${RPM_BUILD_ROOT}/%{_sysconfdir}/knox/conf
cp -rp ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/conf/* ${RPM_BUILD_ROOT}/%{_sysconfdir}/knox/conf.dist
cp -rp ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/data/* ${RPM_BUILD_ROOT}/%{_localstatedir}/lib/knox/data
mkdir -p  ${RPM_BUILD_ROOT}/%{_localstatedir}/lib/knox/data/security
mkdir -p  ${RPM_BUILD_ROOT}/%{_localstatedir}/lib/knox/data/deployments
rm -rf ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/data
rm -rf ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/conf
rm -rf ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/pids
rm -rf ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/logs
ln -sf %{_localstatedir}/lib/knox/data ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/data
ln -sf %{_localstatedir}/run/knox  ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/pids
ln -sf %{_localstatedir}/log/knox  ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/logs
ln -sf %{_sysconfdir}/knox/conf ${RPM_BUILD_ROOT}/%{knox_libdirname}/knox/conf

#######################
#### FILES SECTION ####
#######################

%files
%defattr(-,root,root,755)
%{knox_libdirname}/knox
%{_sysconfdir}/init.d/%{knox_name}
%defattr(-,knox,knox,755)
%{_localstatedir}/log/knox
%{_localstatedir}/lib/knox/data
%{_localstatedir}/run/knox
%{_sysconfdir}/knox/conf.dist
%config(noreplace) %{_sysconfdir}/knox/conf

%pre
######################
getent group knox 2>&1 > /dev/null || /usr/sbin/groupadd -r knox
getent group hadoop 2>&1 > /dev/null || /usr/sbin/groupadd -r hadoop
getent passwd knox 2>&1 > /dev/null || /usr/sbin/useradd -c "KNOX" -s /bin/bash -g knox -G hadoop -r -d /var/lib/knox knox 2> /dev/null || :
