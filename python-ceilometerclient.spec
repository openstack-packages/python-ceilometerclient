Name:             python-ceilometerclient
Version:          1.0.0
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Ceilometer

Group:            Development/Languages
License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python2-devel

Requires:         python-setuptools
Requires:         python-argparse
Requires:         python-prettytable >= 0.6
Requires:         python-prettytable < 0.7
Requires:         python-iso8601 >= 0.1.4
Requires:         python-keystoneclient >= 0.1.2

#
# patches_base=0.0.10.d84fd99
#

%description
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).


%package doc
Summary:          Documentation for OpenStack Ceilometer API Client
Group:            Documentation

BuildRequires:    python-sphinx

%description      doc
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).

This package contains auto-generated documentation.


%prep
%setup -q

# Remove bundled egg-info.
rm -rf python_novaclient.egg-info

# Let RPM handle deps.
# TODO: Have the following handle multi line entries.
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# MANIFEST.in contains mostly non-existent files, delete it.
rm -f 'MANIFEST.in'


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -rf %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo

%files
%doc README.md
%doc LICENSE
%{_bindir}/ceilometer
%{python_sitelib}/ceilometerclient
%{python_sitelib}/*.egg-info

%files doc
%doc html

%changelog
* Mon Apr 01 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.0
- Update to upstream version 1.0.0.
- Added Requires: python-keystoneclient >= 0.1.2.

* Tue Mar 26 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.0.10-0.2.gitd84fd99
- Add BuildRequires: python2-devel.

* Tue Mar 26 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.0.10-0.1.gitd84fd99
- Initial package based on python-novaclient.
