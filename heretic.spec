Summary:	Heretic for Linux
Summary(pl):	Heretic dla Linuksa
Name:		heretic
Version:	1.2
Release:	1
Group:		Applications/Games
License:	Activision/Raven, see Documentation
Source0:	http://heretic.linuxgames.com/heretic/src/gl%{name}-%{version}.tar.gz
# NoSource0-md5: fafb739195bfbf2dd035070ec0792d4e
Source1:	http://heretic.linuxgames.com/wad/%{name}_share.tar.bz2
# Source1-md5:	d5f9264dcd42f5ef8ebedfd020e8f499
Source2:	%{name}.png
# it seems to be non-distributable (see documentation)
NoSource:	0
Patch0:		%{name}-paths.patch
Patch1:		%{name}-nosysio.patch
Patch2:		%{name}-duplicatecase.patch
URL:		http://heretic.linuxgames.com/
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	XFree86-devel
%ifarch %{ix86} alpha
BuildRequires:	svgalib-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
# dlopens libGL.so
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

%package data-shareware
Summary:	Heretic for Linux - shareware version of data (WAD file)
Summary(pl):	Heretic dla Linuksa - wersja shareware danych (pliku WAD)
Group:		Applications/Games
Requires:	%{name}-common = %{version}

%description data-shareware
Heretic for Linux - shareware version of data (WAD file).

%description data-shareware -l pl
Heretic dla Linuksa - wersja shareware danych (pliku WAD).

%prep
%setup -q -n gl%{name}-%{version} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -f .depend

%build
OPT="%{rpmcflags} %{!?debug:-fomit-frame-pointer} -DHAVE_ALLOCA_H"
%ifarch alpha ia64 ppc64 sparc64 x86_64
OPT="$OPT -D__64BIT__"
%else
OPT="$OPT -D__32BIT__"
%endif
%ifarch m68k ppc ppc64 sparc sparc64 sparcv9
OPT="$OPT -D__BIG_ENDIAN__"
%endif
%ifarch %{ix86}
OPT="$OPT %{!?debug:-DINLINE_FIXED}"
%endif
%ifarch arm sparc sparc64 sparcv9
OPT="$OPT -DPACKED=\\\"__attribute__ ((packed))\\\""
%endif
%ifarch arm
OPT="$OPT -fsigned-char"
%endif
# Make the other versions
%ifarch %{ix86} alpha
%{__make} fastx11 x11 sdl vga sndserver musserver \
	CC="%{__cc}" \
	WANT_OGL=no \
	COPT.arch="$OPT"
%else
%{__make} fastx11 x11 sdl sndserver musserver \
	CC="%{__cc}" \
	WANT_OGL=no \
	COPT.arch="$OPT"
%endif

# Make OpenGL version
rm -f *.o graphics/*.o
%{__make} -C opengl/sgi-si/libtess sgi-libtess \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%{__make} glheretic \
	CC="%{__cc}" \
	WANT_OGL=yes \
	COPT.arch="$OPT -DGLU_VERSION_1_2"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/%{name}} \
	$RPM_BUILD_ROOT{%{_libdir}/games/%{name},%{_desktopdir},%{_pixmapsdir}}
%ifarch %{ix86} alpha
hvers="xa x sdl vga gl"
%else
hvers="xa x sdl gl"
%endif

for i in $hvers; do
	install ${i}%{name} $RPM_BUILD_ROOT%{_bindir}
	desktopfile="$RPM_BUILD_ROOT%{_desktopdir}/${i}%{name}.desktop"
	echo "[Desktop Entry]\nName=Heretic ($i)\nComment=Linux Heretic \
	\nExec=%{_bindir}/${i}%{name}\nIcon=%{name}.png\nTerminal=false \
	\nType=Application\nCategories=Game;FirstPersonGame;" > $desktopfile
done

install -m 755 musserver sndserver $RPM_BUILD_ROOT%{_libdir}/games/%{name}
install heretic_share.wad $RPM_BUILD_ROOT%{_datadir}/games/%{name}
# Currently, this is only needed for the OpenGL version
install *.raw $RPM_BUILD_ROOT%{_datadir}/games/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

mv -f doc/End* doc/EndUserLicense-HereticSourceCode.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/x%{name}
%{_desktopdir}/x%{name}.desktop

%files fastx11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xa%{name}
%{_desktopdir}/xa%{name}.desktop

%ifarch %{ix86} alpha
%files vga
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vga%{name}
%{_desktopdir}/vga%{name}.desktop
%endif

%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sdl%{name}
%{_desktopdir}/sdl%{name}.desktop

%files gl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gl%{name}
%{_desktopdir}/gl%{name}.desktop

%files common
%defattr(644,root,root,755)
%doc doc/*
%dir %{_datadir}/games/%{name}
%{_datadir}/games/%{name}/*.raw
%attr(755,root,root) %{_libdir}/games/%{name}
%{_pixmapsdir}/*

%files data-shareware
%defattr(644,root,root,755)
%{_datadir}/games/%{name}/heretic_share.wad
