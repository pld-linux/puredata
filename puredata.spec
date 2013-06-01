# TODO: portaudio, portmidi
# TODO: optflags for extra
Summary:	Pd - free real-time computer music software package resembling Max
Summary(pl.UTF-8):	Pd - darmowy pakiet do muzyki w czasie rzeczywistym podobny do Maksa
Name:		puredata
Version:	0.44.0
Release:	0.1
License:	BSD, only expr plugin on GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/pure-data/pd-0.40-2.src.tar.gz
# Source0-md5:	2622e12b6fa0bd69db9732972e953afb
Patch0:		%{name}-makefile.patch
URL:		http://puredata.info/
BuildRequires:	alsa-lib-devel
BuildRequires:	fftw-devel
BuildRequires:	jack-audio-connection-kit-devel
#BuildRequires:	portaudio-devel
#BuildRequires:	portmidi-devel
BuildRequires:	tk-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pd - free real-time computer music software package resembling Max.

%description -l pl.UTF-8
Pd - darmowy pakiet do muzyki w czasie rzeczywistym podobny do Maksa.

%package devel
Summary:	Header file for Pd
Summary(pl.UTF-8):	Plik nagłówkowy Pd
Group:		Development/Libraries
# doesn't require base

%description devel
Header file for Pd.

%description devel -l pl.UTF-8
Plik nagłówkowy Pd.

%prep
%setup -q -n pd-0.40-2
%patch0 -p0

cp extra/expr~/README.txt README-expr.txt

%build
cd src
%configure \
	--with-fftw \
	--with-jack \
	--with-alsa \
# --with-portaudio --with-portmidi (fix to use system lisb)
%{__make} \
	CC="%{__cc}" \
	MORECFLAGS=-D_LARGEFILE64_SOURCE

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=$RPM_BUILD_ROOT%{_libdir}

mv -f $RPM_BUILD_ROOT%{_libdir}/pd/doc pd-doc
find $RPM_BUILD_ROOT%{_libdir}/pd/extra -name '*.[ch]*' -or -name 'makefile' -or -name '*_o' | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt README-expr.txt src/CHANGELOG.txt
%attr(755,root,root) %{_bindir}/pd
%attr(755,root,root) %{_bindir}/pdreceive
%attr(755,root,root) %{_bindir}/pdsend
%dir %{_libdir}/pd
%dir %{_libdir}/pd/bin
# two following R: tcl/tk
%attr(755,root,root) %{_libdir}/pd/bin/pd-gui
%{_libdir}/pd/bin/pd.tk
%attr(755,root,root) %{_libdir}/pd/bin/pd-watchdog
%dir %{_libdir}/pd/extra
%{_libdir}/pd/extra/*.pd
%dir %{_libdir}/pd/extra/bonk~
%attr(755,root,root) %{_libdir}/pd/extra/bonk~/bonk~.pd_linux
%{_libdir}/pd/extra/bonk~/*.pd
%{_libdir}/pd/extra/bonk~/*.txt
%dir %{_libdir}/pd/extra/choice
%attr(755,root,root) %{_libdir}/pd/extra/choice/choice.pd_linux
%{_libdir}/pd/extra/choice/*.pd
%dir %{_libdir}/pd/extra/expr~
%attr(755,root,root) %{_libdir}/pd/extra/expr~/*.pd_linux
%dir %{_libdir}/pd/extra/fiddle~
%attr(755,root,root) %{_libdir}/pd/extra/fiddle~/fiddle~.pd_linux
%{_libdir}/pd/extra/fiddle~/*.pd
%dir %{_libdir}/pd/extra/loop~
%attr(755,root,root) %{_libdir}/pd/extra/loop~/loop~.pd_linux
%{_libdir}/pd/extra/loop~/*.pd
%dir %{_libdir}/pd/extra/lrshift~
%attr(755,root,root) %{_libdir}/pd/extra/lrshift~/lrshift~.pd_linux
%{_libdir}/pd/extra/lrshift~/*.pd
%dir %{_libdir}/pd/extra/pique
%attr(755,root,root) %{_libdir}/pd/extra/pique/pique.pd_linux
%{_libdir}/pd/extra/pique/*.pd
%dir %{_libdir}/pd/extra/sigmund~
%attr(755,root,root) %{_libdir}/pd/extra/sigmund~/sigmund~.pd_linux
%{_libdir}/pd/extra/sigmund~/*.pd
%{_mandir}/man1/pd.1*
%{_mandir}/man1/pdreceive.1*
%{_mandir}/man1/pdsend.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/m_pd.h
