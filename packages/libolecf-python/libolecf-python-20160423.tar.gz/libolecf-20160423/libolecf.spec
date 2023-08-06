Name: libolecf
Version: 20160423
Release: 1
Summary: Library to access the Object Linking and Embedding (OLE) Compound File (CF) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libolecf/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
                
                

%description
libolecf is a library to access the Object Linking and Embedding (OLE) Compound File (CF) format

%package devel
Summary: Header files and libraries for developing applications for libolecf
Group: Development/Libraries
Requires: libolecf = %{version}-%{release}

%description devel
Header files and libraries for developing applications for libolecf.

%package tools
Summary: Several tools for accessing the Object Linking and Embedding (OLE) Compound Files (CF)
Group: Applications/System
Requires: libolecf = %{version}-%{release}  fuse-libs
BuildRequires:  fuse-devel

%description tools
Several tools for accessing the Object Linking and Embedding (OLE) Compound Files (CF)

%package python
Summary: Python 2 bindings for libolecf
Group: System Environment/Libraries
Requires: libolecf = %{version}-%{release} python
BuildRequires: python-devel

%description python
Python 2 bindings for libolecf

%package python3
Summary: Python 3 bindings for libolecf
Group: System Environment/Libraries
Requires: libolecf = %{version}-%{release} python3
BuildRequires: python3-devel

%description python3
Python 3 bindings for libolecf

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libolecf.pc
%{_includedir}/*
%{_mandir}/man3/*

%files tools
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_bindir}/olecfexport
%attr(755,root,root) %{_bindir}/olecfinfo
%attr(755,root,root) %{_bindir}/olecfmount
%{_mandir}/man1/*

%files python
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files python3
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%changelog
* Sat Apr 23 2016 Joachim Metz <joachim.metz@gmail.com> 20160423-1
- Auto-generated

