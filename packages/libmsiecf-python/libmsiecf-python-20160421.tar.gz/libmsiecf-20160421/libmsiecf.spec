Name: libmsiecf
Version: 20160421
Release: 1
Summary: Library to access the MSIE Cache File (index.dat) format.
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libmsiecf/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
             
               

%description
libmsiecf is a library to access the MSIE Cache File (index.dat) format.

%package devel
Summary: Header files and libraries for developing applications for libmsiecf
Group: Development/Libraries
Requires: libmsiecf = %{version}-%{release}

%description devel
Header files and libraries for developing applications for libmsiecf.

%package tools
Summary: Several tools for reading MSIE Cache File (index.dat).
Group: Applications/System
Requires: libmsiecf = %{version}-%{release} 
 

%description tools
Several tools for reading MSIE Cache File (index.dat).

%package python
Summary: Python 2 bindings for libmsiecf
Group: System Environment/Libraries
Requires: libmsiecf = %{version}-%{release} python
BuildRequires: python-devel

%description python
Python 2 bindings for libmsiecf

%package python3
Summary: Python 3 bindings for libmsiecf
Group: System Environment/Libraries
Requires: libmsiecf = %{version}-%{release} python3
BuildRequires: python3-devel

%description python3
Python 3 bindings for libmsiecf

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
%{_libdir}/pkgconfig/libmsiecf.pc
%{_includedir}/*
%{_mandir}/man3/*

%files tools
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_bindir}/msiecfexport
%attr(755,root,root) %{_bindir}/msiecfinfo
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
* Thu Apr 21 2016 Joachim Metz <joachim.metz@gmail.com> 20160421-1
- Auto-generated

