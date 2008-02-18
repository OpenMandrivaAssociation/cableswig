
Summary:	Used to create interfaces to interpreted languages
Name:		cableswig
Version:	3.2.0
Release:	%mkrel 3
License:	BSDish
Group:		Development/C++
URL:		http://www.itk.org
Source0:	http://ovh.dl.sourceforge.net/sourceforge/itk/CableSwig-ITK-%{version}.tar.bz2
# Patch0:		CableSwig-libdir.patch
# Patch1:         cableswig-cmake-2.4.4+.patch
Patch2:		pystrings.patch
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

%setup -q -n CableSwig-ITK-%{version}
# %patch0 -p1
# %patch1 -p0
%patch2 -p0
find -name CVS -type d | xargs rm -rf

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_BUILD_TYPE:STRING=Release \
      -DCMAKE_SKIP_RPATH:BOOL=ON \
      -DLIB_DIRECTORY_NAME:STRING=%{_lib} \
      -DCMAKE_CXX_COMPILER:PATH=%{_bindir}/c++ \
      -DCMAKE_C_COMPILER:PATH=%{_bindir}/gcc \
      -DSWIG_LIB_INSTALL:PATH=%{_libdir}/CableSwig/SWIGLib/ \
..

%make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

# fix lib path
%if "%{_lib}" == "lib64"
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/%{_libdir}
%endif

# mv gccxml to std path
mv $RPM_BUILD_ROOT/%{_libdir}/CableSwig/share $RPM_BUILD_ROOT/%{_prefix}
mv $RPM_BUILD_ROOT/%{_libdir}/CableSwig/bin $RPM_BUILD_ROOT/%{_bindir}

# and another bug: some files are not copied
cp -rf ../SWIG/Lib/* $RPM_BUILD_ROOT/%{_libdir}/CableSwig/SWIGLib

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
rm -rf $RPM_BUILD_ROOT

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





