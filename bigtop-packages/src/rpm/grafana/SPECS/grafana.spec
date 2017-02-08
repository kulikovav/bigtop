%define 	   debug_package %{nil}

Name:              grafana
Version:           %{grafana_version}
Release:           %{grafana_release}
Summary:           Grafana provides a powerful and elegant way to create, explore, and share dashboards and data with your team and the world. 
Group:             Application/Internet
License:           MIT
URL:               http://grafana.org
Buildroot: 	   %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Source0:           %{name}-%{grafana_base_version}.tar.gz 
Source1:	   install_%{name}.sh
BuildArch:         x86_64
Requires:          initscripts, daemonize
Provides:          grafana = %{grafana_version}

%description
Grafana is most commonly used for visualizing time series data for Internet infrastructure and application analytics but many use it in other domains including industrial sensors, home automation, weather, and process control.

%prep
%setup -qn grafana-%{grafana_base_version}-%{grafana_buildstamp}

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
