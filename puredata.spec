Summary:	Pd - graphical programming environment for real-time audio synthesis etc.
Summary(pl.UTF-8):	Pd - środowisko do graficznego programowania syntezy dźwięku itp.
Name:		puredata
Version:	0.48.1
Release:	1
License:	GPL v2+ (expr plugin), BSD (the rest)
Group:		Libraries
Source0:	http://msp.ucsd.edu/Software/pd-0.48-1.src.tar.gz
# Source0-md5:	8c4deff54b47a10d2f55e363022cc634
Patch0:		findprogdir.patch
URL:		http://puredata.info/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	fftw3-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libtool
BuildRequires:	portaudio-devel >= 19
#BuildRequires:	portmidi-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# puredata actually sanitizes the format string before use
# and the usual '%s', trick would break '%%' format strings
%define		filterout_c -Werror=format-security

%description
Pd is a graphical programming environment for real-time audio
synthesis and related applications. It supports a rich set of
real-time control and I/O features.

%description -l pl.UTF-8
Pd to środowisko do graficznego programowania dla syntezy dźwięku w
czasie rzeczywistym i zbliżonych zastosowań. Obsługuje bogaty zbiór
kontrolek czasu rzeczywistego oraz funkcji we/wy.

%package gui
Summary:	Tcl/Tk based graphical user interface for Pd
Summary(pl.UTF-8):	Oparty na Tcl/Tk graficzny interfejs użytkownika do Pd
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	tcl >= 8.3
Requires:	tk >= 8.3

%description gui
Tcl/Tk based graphical user interface for Pd.

%description gui -l pl.UTF-8
Oparty na Tcl/Tk graficzny interfejs użytkownika do Pd.

%package devel
Summary:	Header files for Pd
Summary(pl.UTF-8):	Pliki nagłówkowe Pd
Group:		Development/Libraries
# doesn't require base

%description devel
Header files for Pd.

%description devel -l pl.UTF-8
Pliki nagłówkowe Pd.

%package doc
Summary:	Documentation and examples for Pd
Summary(pl.UTF-8):	Dokumentacja i przykłady do Pd
Group:		Documentation

%description doc
Documentation and examples for Pd.

%description doc -l pl.UTF-8
Dokumentacja i przykłady do Pd.

%prep
%setup -q -n pd-0.48-1

%patch0 -p1

cp extra/README.txt README-extra.txt
for f in extra/*/README.txt ; do
	cp "$f" README-"$(basename $(dirname "$f"))".txt
done

%build
%{__libtoolize}
%{__aclocal} -I m4/generated -I m4
%{__autoconf}
%{__automake}
%configure CPPFLAGS="%{rpmcppflags} -DPROGDIR='\"%{_libdir}/pd\"'" \
	--enable-fftw \
	--enable-jack \
	--enable-alsa \
	--without-local-portmidi \
	--without-local-portaudio
# note: --enable-portmidi conflicts with OSS (which is enabled on Linux)

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/pd/extra/*/*.la

install -d $RPM_BUILD_ROOT%{_docdir}
mv -f $RPM_BUILD_ROOT%{_libdir}/pd/doc $RPM_BUILD_ROOT%{_docdir}/puredata-doc
ln -s %{_docdir}/puredata-doc $RPM_BUILD_ROOT%{_libdir}/pd/doc

# 'Symlink points to BuildRoot'
ln -sf %{_bindir}/pd $RPM_BUILD_ROOT%{_libdir}/pd/bin/pd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt README-*.txt src/CHANGELOG.txt
%attr(755,root,root) %{_bindir}/pd
%attr(755,root,root) %{_bindir}/pdreceive
%attr(755,root,root) %{_bindir}/pdsend
%dir %{_libdir}/pd
%dir %{_libdir}/pd/bin
%attr(755,root,root) %{_libdir}/pd/bin/pd
%attr(755,root,root) %{_libdir}/pd/bin/pd-watchdog
%dir %{_libdir}/pd/extra
%{_libdir}/pd/extra/*.pd
%dir %{_libdir}/pd/extra/bob~
%attr(755,root,root) %{_libdir}/pd/extra/bob~/bob~.pd_linux
%{_libdir}/pd/extra/bob~/*.pd
%dir %{_libdir}/pd/extra/bonk~
%attr(755,root,root) %{_libdir}/pd/extra/bonk~/bonk~.pd_linux
%{_libdir}/pd/extra/bonk~/*.pd
%{_libdir}/pd/extra/bonk~/templates.txt
%dir %{_libdir}/pd/extra/choice
%attr(755,root,root) %{_libdir}/pd/extra/choice/choice.pd_linux
%{_libdir}/pd/extra/choice/choice-help.pd
%dir %{_libdir}/pd/extra/fiddle~
%attr(755,root,root) %{_libdir}/pd/extra/fiddle~/fiddle~.pd_linux
%{_libdir}/pd/extra/fiddle~/fiddle~-help.pd
%dir %{_libdir}/pd/extra/loop~
%attr(755,root,root) %{_libdir}/pd/extra/loop~/loop~.pd_linux
%{_libdir}/pd/extra/loop~/*.pd
%dir %{_libdir}/pd/extra/lrshift~
%attr(755,root,root) %{_libdir}/pd/extra/lrshift~/lrshift~.pd_linux
%{_libdir}/pd/extra/lrshift~/lrshift~-help.pd
%dir %{_libdir}/pd/extra/pd~
%attr(755,root,root) %{_libdir}/pd/extra/pd~/pd*.pd_linux
%{_libdir}/pd/extra/pd~/pd~-*.pd
%dir %{_libdir}/pd/extra/pique
%attr(755,root,root) %{_libdir}/pd/extra/pique/pique.pd_linux
%{_libdir}/pd/extra/pique/pique-help.pd
%dir %{_libdir}/pd/extra/sigmund~
%attr(755,root,root) %{_libdir}/pd/extra/sigmund~/sigmund~.pd_linux
%{_libdir}/pd/extra/sigmund~/sigmund~-help.pd
%dir %{_libdir}/pd/extra/stdout
%attr(755,root,root) %{_libdir}/pd/extra/stdout/stdout.pd_linux
%{_libdir}/pd/extra/stdout/stdout-help.pd
%{_libdir}/pd/startup
%{_mandir}/man1/pd.1*
%{_mandir}/man1/pdreceive.1*
%{_mandir}/man1/pdsend.1*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pd-gui
%dir %{_libdir}/pd/po
%lang(af) %{_libdir}/pd/po/af.msg
%lang(az) %{_libdir}/pd/po/az.msg
%lang(be) %{_libdir}/pd/po/be.msg
%lang(bg) %{_libdir}/pd/po/bg.msg
%lang(de) %{_libdir}/pd/po/de.msg
%lang(el) %{_libdir}/pd/po/el.msg
%lang(en_CA) %{_libdir}/pd/po/en_ca.msg
%lang(es) %{_libdir}/pd/po/es.msg
%lang(eu) %{_libdir}/pd/po/eu.msg
%lang(fr) %{_libdir}/pd/po/fr.msg
%lang(gu) %{_libdir}/pd/po/gu.msg
%lang(he) %{_libdir}/pd/po/he.msg
%lang(hi) %{_libdir}/pd/po/hi.msg
%lang(hu) %{_libdir}/pd/po/hu.msg
%lang(it) %{_libdir}/pd/po/it.msg
%lang(pa) %{_libdir}/pd/po/pa.msg
%lang(pt_BR) %{_libdir}/pd/po/pt_br.msg
%lang(pt) %{_libdir}/pd/po/pt_pt.msg
%lang(sq) %{_libdir}/pd/po/sq.msg
%lang(sv) %{_libdir}/pd/po/sv.msg
%lang(vi) %{_libdir}/pd/po/vi.msg
%dir %{_libdir}/pd/tcl
%attr(755,root,root) %{_libdir}/pd/tcl/pd-gui.tcl
%{_libdir}/pd/tcl/AppMain.tcl
%{_libdir}/pd/tcl/apple_events.tcl
%{_libdir}/pd/tcl/dialog_*.tcl
%{_libdir}/pd/tcl/helpbrowser.tcl
%{_libdir}/pd/tcl/opt_parser.tcl
%{_libdir}/pd/tcl/pd_*.tcl
%{_libdir}/pd/tcl/pdtk_*.tcl
%{_libdir}/pd/tcl/pdwindow.tcl
%{_libdir}/pd/tcl/pkgIndex.tcl
%{_libdir}/pd/tcl/pkg_mkIndex.tcl
%{_libdir}/pd/tcl/scrollbox*.tcl
%{_libdir}/pd/tcl/wheredoesthisgo.tcl
%{_libdir}/pd/tcl/pd.ico

%files devel
%defattr(644,root,root,755)
%{_includedir}/m_pd.h
%{_includedir}/pd
%{_pkgconfigdir}/pd.pc

%files doc
%defattr(644,root,root,755)
%{_libdir}/pd/doc
%{_docdir}/puredata-doc
