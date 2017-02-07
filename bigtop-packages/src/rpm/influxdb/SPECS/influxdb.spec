%define 	   debug_package %{nil}
%define		   pkg_release 1

Name:              influxdb
Version:           %{influxdb_version}
Release:           %{influxdb_release}
Summary:           Scalable datastore for metrics, events, and real-time analytics.
Group:             Application/Databases
License:           MIT
URL:               https://influxdata.com
Buildroot: 	   %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Source0:           %{name}-%{influxdb_base_version}.tar.gz 
Source1:	   install_%{name}.sh
BuildArch:         x86_64
Requires:          initscripts, daemonize
Provides:          influxdb = %{influxdb_version}

%description
InfluxDB is an open source time series database with no external dependencies. It's useful for recording metrics, events, and performing analytics.

%prep
%setup -qn influxdb-%{influxdb_base_version}-%{pkg_release}

%build

%install
rm -rf %{buildroot}
sh %{SOURCE1} --build-dir=. --prefix=$RPM_BUILD_ROOT

%pre

%post

%clean
%{__rm} -rf %{buildroot}

%files

%defattr(-,root,root,-)
/opt/%{name}
