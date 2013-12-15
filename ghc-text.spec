#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	text
Summary:	A Haskell library for manipulation of Unicode text
Summary(pl.UTF-8):	Biblioteka Haskella do operacji na tekście kodowanym w Unicode
Name:		ghc-%{pkgname}
Version:	1.0.0.0
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/text
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	6c76d0b7a6e5d2f4e0d0359b28e4a3e2
URL:		http://hackage.haskell.org/package/text
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array >= 0.3
BuildRequires:	ghc-base >= 4.2
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-deepseq >= 1.1.0.0
BuildRequires:	ghc-ghc-prim >= 0.2
BuildRequires:	ghc-integer-gmp >= 0.2
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof >= 0.3
BuildRequires:	ghc-base-prof >= 4.2
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-deepseq-prof >= 1.1.0.0
BuildRequires:	ghc-ghc-prim-prof >= 0.2
BuildRequires:	ghc-integer-gmp-prof >= 0.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-array >= 0.3
Requires:	ghc-base >= 4.2
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-deepseq >= 1.1.0.0
Requires:	ghc-ghc-prim >= 0.2
Requires:	ghc-integer-gmp >= 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package provides the Data.Text library, a library for the space-
and time-efficient manipulation of Unicode text in Haskell.

%description -l pl.UTF-8
Ten pakiet dostarcza bibliotekę Data.Text - służącą do wydajnych pod
względem objętości i czasu operacji na tekście kodowanym w Unicode z
poziomu Haskella.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof >= 0.3
Requires:	ghc-base-prof >= 4.2
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-deepseq-prof >= 1.1.0.0
Requires:	ghc-ghc-prim-prof >= 0.2
Requires:	ghc-integer-gmp-prof >= 0.2

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for %{pkgname} ghc package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname} ghc package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown changelog
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HStext-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStext-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Encoding
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Encoding/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Encoding/Fusion
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Encoding/Fusion/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Fusion
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Fusion/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/IO
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/IO/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder/Int
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder/Int/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder/RealFloat
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder/RealFloat/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Encoding
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Encoding/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Unsafe
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Unsafe/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStext-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Encoding/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Encoding/Fusion/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Fusion/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/IO/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder/Int/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder/RealFloat/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Encoding/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Unsafe/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
