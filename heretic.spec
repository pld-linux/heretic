Summary:	Heretic for Linux
Summary(pl):	Heretic dla Linuksa
Name:		heretic
Version:	1.1
Release:	1
Group:		Applications/Games
License:	Activision/Raven, see Documentation
URL:		http://heretic.linuxgames.com/
Source0:	http://heretic.linuxgames.com/heretic/src/gl%{name}-%{version}.tar.gz
Source1:	http://heretic.linuxgames.com/wad/%{name}_share.tar.bz2
# it seems to be non-distributable (see documentation)
NoSource:	0
Patch0:		%{name}-paths.patch
Patch1:		%{name}-glcallback.patch
BuildRequires:	XFree86-devel
%ifarch %{ix86}
BuildRequires:	svgalib-devel
%endif
BuildRequires:	SDL-devel
BuildRequires:	OpenGL-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		%{_prefix}/games
%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Heretic for Linux.

%description -l pl
Heretic dla Linuksa.

%package x11
Summary:	Heretic for Linux - X11 version
Summary(pl):	Heretic dla Linuksa - wersja pod X11
Group:		X11/Applications/Games
Requires:	%{name}-common = %{version}

%description x11
Heretic for Linux (X11 version).

%description x11 -l pl
Heretic dla Linuksa (wersja pod X11).

%package fastx11
Summary:	Heretic for Linux - Accelerated X11 version
Summary(pl):	Heretic dla Linuksa - przyspieszona wersja pod X11
Group:		X11/Applications/Games
Requires:	%{name}-common = %{version}

%description fastx11
Heretic for Linux (accelerated X11 version).

%description fastx11 -l pl
Heretic dla Linuksa (przyspieszona wersja pod X11).

%package vga
Summary:	Heretic for Linux - SVGA version
Summary(pl):	Heretic dla Linuksa - wersja SVGA
Group:		Applications/Games
Requires:	%{name}-common = %{version}

%description vga
Heretic for Linux (svgalib version).

%description vga -l pl
Heretic dla Linuksa (wersja svgalib).

%package sdl
Summary:	Heretic for Linux - SDL version
Summary(pl):	Heretic dla Linuksa - wersja SDL
Group:		Applications/Games
Requires:	%{name}-common = %{version}

%description sdl
Heretic for Linux (SDL version).

%description sdl -l pl
Heretic dla Linuksa (wersja SDL).

%package gl
Summary:	Heretic for Linux - OpenGL version
Summary(pl):	Heretic dla Linuksa - wersja OpenGL
Group:		Applications/Games
Requires:	%{name}-common = %{version}
Requires:	OpenGL

%description gl
Heretic for Linux (OpenGL version).

%description gl -l pl
Heretic dla Linuksa (wersja OpenGL).

%package common
Summary:	Heretic for Linux - shared files
Summary(pl):	Heretic dla Linuksa - wspólne pliki
Group:		Applications/Games

%description common
Heretic is a supernatural blast-fest that is the most realistic,
action-packed fantasy combat computer game for the PC. Created by the
graphic masters at Raven Software in concert with the technical gurus
of id Software, Heretic adds new levels of play and graphic wonder to
the tried and true DOOM gaming environment.

This package contains Heretic common files.

%description common -l pl
Heretic jest realistyczn± gr± walki w ¶wiecie fantasy. Stworzona
zosta³a przez grafików Raven Software w porozumieniu z technikami Id
Software. Heretic daje nowe poziomy gry oraz now± grafikê do
wypróbowanego ¶rodowiska DOOMa.

Ten pakiet zawiera wspólne pliki dla wszystkich wersji Heretica pod
Linuksa.

%prep
%setup -q -n gl%{name}-%{version} -a1
%patch0 -p1
%patch1 -p1

%build
OPT="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"
%ifarch %{ix86}
OPT="$OPT -D__32BIT__ -DHAVE_ALLOCA_H -DINLINE_FIXED"
%endif
%ifarch m68k
OPT="$OPT -D__BIG_ENDIAN__ -D__32BIT__ -DHAVE_ALLOCA_H"
%endif
%ifarch alpha
OPT="$OPT -D__64BIT__ -DHAVE_ALLOCA_H"
%endif
%ifarch arm
OPT="$OPT -D__32BIT__ -fsigned-char -DHAVE_ALLOCA_H -DPACKED=\\\"__attribute__ ((packed))\\\""
%endif
%ifarch sparc
OPT="$OPT -D__32BIT__ -D__BIG_ENDIAN__ -DHAVE_ALLOCA_H -DPACKED=\\\"__attribute__ ((packed))\\\""
%endif
# Make the other versions
%ifarch %{ix86}
%{__make} WANT_OGL=no COPT.arch="$OPT" fastx11 x11 sdl vga sndserver musserver
%else
%{__make} WANT_OGL=no COPT.arch="$OPT" fastx11 x11 sdl sndserver musserver
%endif
# Make OpenGL version
rm -f $(grep -l GL_HERETIC $(find . -name \*.c) | sed 's/\.c/.o/g')
%{__make} WANT_OGL=yes COPT.arch="$OPT -DGLU_VERSION_1_2" glheretic

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/%{name}} \
	$RPM_BUILD_ROOT{%{_libdir}/games/%{name},%{_applnkdir}/Games}
%ifarch %{ix86}
hvers="xa x sdl vga gl"
%else
hvers="xa x sdl gl"
%endif
for i in $hvers; do
	install ${i}%{name} $RPM_BUILD_ROOT%{_bindir}
	echo > $RPM_BUILD_ROOT%{_applnkdir}/Games/${i}%{name}.desktop <<EOF
[Desktop Entry]
Name=Heretic
Comment=Linux Heretic
TryExec=%{_bindir}/${i}%{name}
Exec=%{_bindir}/${i}%{name}
Terminal=0
Type=Application
EOF
# Menu entry for Mandrake/KDE
done
install -m 755 musserver sndserver $RPM_BUILD_ROOT%{_libdir}/games/%{name}
install heretic_share.wad $RPM_BUILD_ROOT%{_datadir}/games/%{name}
# Currently, this is only needed for the OpenGL version
install *.raw $RPM_BUILD_ROOT%{_datadir}/games/%{name}

mv -f doc/End* doc/EndUserLicense-HereticSourceCode.txt
gzip -9nf doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/x%{name}
%{_applnkdir}/Games/x%{name}.desktop

%files fastx11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xa%{name}
%{_applnkdir}/Games/xa%{name}.desktop

%ifarch %{ix86}
%files vga
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vga%{name}
%endif

%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sdl%{name}
%{_applnkdir}/Games/sdl%{name}.desktop

%files gl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gl%{name}
%{_applnkdir}/Games/gl%{name}.desktop

%files common
%defattr(644,root,root,755)
%doc doc/*.gz
%{_datadir}/games/%{name}
%attr(755,root,root) %{_libdir}/games/%{name}
