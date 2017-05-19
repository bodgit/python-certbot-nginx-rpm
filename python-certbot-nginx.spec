%global pyname certbot-nginx

# On fedora use python3 for certbot
%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:       python-%{pyname}
Version:    0.14.1
Release:    1%{?dist}
Summary:    The nginx plugin for certbot

License:    ASL 2.0
URL:        https://pypi.python.org/pypi/certbot-nginx
Source0:    https://files.pythonhosted.org/packages/source/c/%{pyname}/%{pyname}-%{version}.tar.gz

Patch0:         allow-old-setuptools.patch

BuildArch:      noarch

BuildRequires: python2-devel

%if %{with python3}
BuildRequires:  python3-devel
%endif

#For running tests
BuildRequires: python2-certbot = %{version}
%if 0%{?rhel}
BuildRequires: pyparsing
%else
BuildRequires: python2-pyparsing
%endif

%if %{with python3}
BuildRequires: python3-certbot = %{version}
BuildRequires: python3-pyparsing
%endif

%description
Plugin for certbot that allows for automatic configuration of ngnix

%package -n python2-%{pyname}
# Provide the name users expect as a certbot plugin
Provides:      %{pyname} = %{version}-%{release}
# Although a plugin for the certbot command it's technically
# an extension to the certbot python libraries
Requires:      python2-certbot = %{version}
%if 0%{?rhel}
Requires: pyparsing
%else
Requires: python2-pyparsing
%endif
%if 0%{?fedora}
#Recommend the CLI as that will be the interface most use
Recommends:    certbot = %{version}
%else
Requires:      certbot = %{version}
%endif
Summary:     The nginx plugin for certbot
%{?python_provide:%python_provide python2-%{pyname}}

%description -n python2-%{pyname}
Plugin for certbot that allows for automatic configuration of nginx

%if %{with python3}
%package -n python3-%{pyname}
# Provide the name users expect as a certbot plugin
Provides:      %{pyname} = %{version}-%{release}
# Although a plugin for the certbot command it's technically
# an extension to the certbot python libraries
Requires:      python3-certbot = %{version}
Requires:      python3-pyparsing
%if 0%{?fedora}
#Recommend the CLI as that will be the interface most use
Recommends:    certbot = %{version}
%else
Requires:      certbot = %{version}
%endif
Summary:     The nginx plugin for certbot
%{?python_provide:%python_provide python3-%{pyname}}

%description -n python3-%{pyname}
Plugin for certbot that allows for automatic configuration of nginx
%endif

%prep
%setup -n %{pyname}-%{version}
%if 0%{?rhel}
%patch0 -p1
%endif

%build
%{py2_build}
%if %{with python3}
%py3_build
%endif

%check
%{__python2} setup.py test
%if %{with python3}
%{__python3} setup.py test
%endif


%install
%{py2_install}
%if %{with python3}
%py3_install
%endif

%files -n python2-%{pyname}
%license LICENSE.txt
%doc README.rst
%{python2_sitelib}/certbot_nginx
%exclude %{python2_sitelib}/certbot_nginx/tests
%{python2_sitelib}/certbot_nginx-%{version}*.egg-info

%if %{with python3}
%files -n python3-%{pyname}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/certbot_nginx
%exclude %{python3_sitelib}/certbot_nginx/tests
%{python3_sitelib}/certbot_nginx-%{version}*.egg-info
%endif

%changelog
* Wed May 17 2017 James Hogarth <james.hogarth@gmail.com> - 0.14.1-1
- Update to 0.14.1

* Fri May 12 2017 James Hogarth <james.hogarth@gmail.com> - 0.13.0-1
- Update to 0.14.0
- Remove the tests directory from binary rpm

* Fri Apr 21 2017 James Hogarth <james.hogarth@gmail.com> - 0.13.0-1
- Initial packaging of the plugin
