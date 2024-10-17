
Summary:	Used to create interfaces to interpreted languages
Name:		cableswig
Version:	3.20.0
Release:	4
License:	BSDish
Group:		Development/C++
URL:		https://www.itk.org
Source0:	http://public.kitware.com/pub/itk/v3.20/CableSwig-ITK-%{version}.tar.gz

# From fedora gccxml package
#		Source is created from a cvs checkout
#		Files for the Borland compiler are excluded for license reasons
#		cvs -d:pserver:anoncvs@www.gccxml.org:/cvsroot/GCC_XML co \
#			-D '2011-02-11 23:59:59Z' -d gccxml-20110211 gccxml
#		tar -z -c --exclude CVS --exclude Borland \
#			-f gccxml-20110211.tar.gz gccxml-20110211
Source1:	gccxml-20110211.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	gccxml = 1:%{version}
Provides:	cable
BuildRequires:  cmake

%description
CableSwig is used to create interfaces (i.e. "wrappers") to interpreted
languages such as Tcl and Python. It was created to produce wrappers for ITK
because the toolkit uses C++ structures that SWIG cannot parse (deeply nested
template instantiations). CableSwig is a combination tool that uses  GCC_XML as
the c++ parser. The input files are  Cable style input files. The XML produced
from the Cable/GCC_XML input files are then parsed and feed into a modified
version of  SWIG. SWIG is a software development tool that connects programs
written in C and C++ with a variety of high-level programming languages. It is
used to generate the language bindings to the target language. Currently, Tcl
and Python are supported.

%package -n gccxml
Summary:	The XML output extension to GCC
Group:		Development/C++
Epoch:		1

%description -n gccxml
Development tools that work with programming languages benefit from their
ability to understand the code with which they work at a level comparable to a
compiler. C++ has become a popular and powerful language, but parsing it is a
very challenging problem. This has discouraged the development of tools meant
to work directly with the language. 

There is one open-source C++ parser, the C++ front-end to GCC, which is
currently able to deal with the language in its entirety. The purpose of the
GCC-XML extension is to generate an XML description of a C++ program from GCC's
internal representation. Since XML is easy to parse, other development tools
will be able to work with C++ programs without the burden of a complicated C++
parser. 

GCC-XML was developed by Brad King at Kitware to be used by CABLE, which was
developed as part of the NLM Insight Segmentation and Registration Toolkit
project.

%prep

%setup -q -n CableSwig-%{version} -a1
find -name CVS -type d | xargs rm -rf

rm -fr GCC GCC_XML
mv gccxml-20110211/GCC{,_XML} .

%build
%cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
       -DCMAKE_BUILD_TYPE:STRING=Release \
       -DCMAKE_SKIP_RPATH:BOOL=ON \
       -DLIB_DIRECTORY_NAME:STRING=%{_lib} \
       -DCMAKE_CXX_COMPILER:PATH=%{_bindir}/c++ \
       -DCMAKE_C_COMPILER:PATH=%{_bindir}/gcc
# 3.20.0 has a problem with paralell build when generating yacc scanner
make

%install
rm -fr %{buildroot}
%makeinstall_std -C build

# fix lib path
%if "%{_lib}" == "lib64"
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/%{_libdir}
%endif

# mv gccxml to std path
mv $RPM_BUILD_ROOT/%{_libdir}/CableSwig/share $RPM_BUILD_ROOT/%{_prefix}
mv $RPM_BUILD_ROOT/%{_libdir}/CableSwig/bin/* $RPM_BUILD_ROOT/%{_bindir}
rmdir $RPM_BUILD_ROOT/%{_libdir}/CableSwig/bin

# set correct path
cat > $RPM_BUILD_ROOT/%{_libdir}/CableSwig/CableSwigConfig.cmake <<EOF
SET(CableSwig_VERSION_MAJOR "0")
SET(CableSwig_VERSION_MINOR "1")
SET(CableSwig_VERSION_PATCH "0")

SET(CableSwig_cableidx_EXE "%{_bindir}/cableidx")
SET(CableSwig_cswig_EXE "%{_bindir}/cswig")
SET(CableSwig_gccxml_EXE "%{_bindir}/gccxml")
SET(CableSwig_DEFAULT_LIB "%{_libdir}/CableSwig/SWIGLib")
EOF


%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/CableSwig
%{_bindir}/cableidx
%{_bindir}/cswig

%files -n gccxml
%defattr(-,root,root)
%{_datadir}/gccxml*
%{_datadir}/doc/*
%{_mandir}/man*/*
%{_bindir}/gccxml
%{_bindir}/gccxml_cc1plus


%changelog
* Thu Nov 17 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.20.0-3mdv2012.0
+ Revision: 731255
- Import and replace gccxml source to add support for gcc 4.6.

* Thu Nov 17 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.20.0-2
+ Revision: 731241
- Rebuild.

* Wed Jul 14 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.20.0-1mdv2011.0
+ Revision: 553411
- Update to version 3.20.0.

* Mon Mar 08 2010 Lev Givon <lev@mandriva.org> 3.16.0-1mdv2010.1
+ Revision: 516716
- Update to 3.16.0.

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 3.14.0-2mdv2010.0
+ Revision: 436908
- rebuild

  + Gaëtan Lehmann <glehmann@mandriva.org>
    - 3.14

* Tue Jan 27 2009 Lev Givon <lev@mandriva.org> 3.10.0-1mdv2009.1
+ Revision: 334348
- Update to 3.10.0.

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 3.2.0-3mdv2008.1
+ Revision: 170780
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- fix description-line-too-long
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Aug 27 2007 Gaëtan Lehmann <glehmann@mandriva.org> 3.2.0-2mdv2008.0
+ Revision: 71868
- 3.2.0
- generate code usable with python on x86_64 (patch2)
- stop playing with patches to install cableswig in the right lib dir, and
  try to install it at the right palce by hand


* Sun Jan 07 2007 Gaëtan Lehmann <glehmann@mandriva.org> 3.0.0-2mdv2007.0
+ Revision: 105136
- fix missing .i files

* Sun Dec 17 2006 Gaëtan Lehmann <glehmann@mandriva.org> 3.0.0-1mdv2007.1
+ Revision: 98269
- 3.0.0
- Import cableswig

* Wed Jul 26 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 1:2.8.0-1mdk
- New release 2.8.0

* Thu Apr 27 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.6.0-6mdk
- cableswig requires the same version of gccxml

* Tue Mar 28 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.6.0-5mdk
- no more require swig

* Tue Mar 28 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.6.0-4mdk
- fix SWIGLIB search path

* Sat Mar 25 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.6.0-3mdk
- Patch0: allow to xinstall in lib64 folder on x86_64
- force /usr/bin/c++ and /usr/bin/gcc compilers

* Tue Mar 21 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.6.0-2mdk
- rebuild to sync i586

* Mon Mar 13 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.6.0-1mdk
- New release 2.6.0

* Wed Dec 07 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.4.0-3mdk
- force swig lib location
- really use 2.4.0 !

* Wed Dec 07 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.4.0-2mdk
- rebuild

* Sat Dec 03 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.4.0-1mdk
- New release 2.4.0

* Sat Oct 22 2005 Nicolas L�cureuil <neoclust@mandriva.org> 0.1.0-3.20050805.4mdk
- Fix BuildRequires

* Mon Aug 15 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 0.1.0-3.20050805.3mdk
- rebuild

* Sun Aug 07 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 0.1.0-3.20050805.2mdk
- fix swiglib path
- move lib back to /usr/lib on x86_64
- fix build on i586

* Sat Aug 06 2005 Gaetan Lehmann <glehmann@deborah.mandriva.com> 0.1.0-3.20050805.1mdk
- cvs snapshot

* Sun Jun 12 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 0.1.0-3mdk
- fix x86_64 build
- use mkrel

* Sat Feb 12 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 0.1.0-2mdk
- fix SWIG Lib directory

* Wed Feb 09 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 0.1.0-1mdk
- stable release from itk

* Sun Jan 30 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 0.1.0-0.cvs20050130.1mdk
- initial contrib

