Summary: Heretic for the X Window System
Name: heretic
Version: 1.0.1
Release: 1
URL: http://www.cs.uni-potsdam.de/~wertmann/
Source0: http://www.cs.uni-potsdam.de/~wertmann/heretic/src/linux-heretic-%{version}.tar.gz
Source1: http://www2.ravensoft.com/source/heretic.zip
Patch0: heretic-0.9.5-alpha.patch.gz
Patch1: heretic-0.9.3-glibc21.patch.gz
Patch2: heretic-0.9.1.1-keymap.patch.gz
Patch3: heretic-0.9.5-datapaths.patch.gz
Patch4: heretic-0.9.1.1-noreturn.patch.gz
Patch5: heretic-0.9.5-soundpath.patch.gz
Patch6: heretic-0.9.5-nodebug.patch.gz
Patch7: heretic-0.9.5-make.patch.gz
Copyright: distributable
Group: Games
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Heretic is a supernatural blast-fest that is the most realistic,
action-packed fantasy combat computer game for the PC.  Created
by the graphic masters at Raven Software in concert with the
technical gurus of id Software, Heretic adds new levels of play
and graphic wonder to the tried and true DOOM gaming environment.

%prep
%setup -c
mkdir -p heretic-1.2
unzip -p %{SOURCE1} HTIC_V12.1 HTIC_V12.2 >heretic-1.2/htic_v12.zip
STATUS=$?
if [ $STATUS -ne 0 ]; then
  exit $STATUS
fi
(cd heretic-1.2 && unzip -Lao htic_v12.zip)
STATUS=$?
if [ $STATUS -ne 0 ]; then
  exit $STATUS
fi
chmod -R a+rX,g-w,o-w .

(cd linux-heretic-%{version}
%patch0 -p1 -b .alpha~
%patch1 -p1 -b .glibc21~
%patch2 -p1 -b .keymap~
%patch3 -p1 -b .datapaths~
%patch4 -p1 -b .noreturn~
%patch5 -p1 -b .soundpath~
%patch6 -p1 -b .nodebug~
%patch7 -p1 -b .make~
)
STATUS=$?
if [ $STATUS -ne 0 ]; then
  exit $STATUS
fi

find . -name "*~" -print0 | xargs -0 rm -f

%build
make -C linux-heretic-%{version} "COPT.arch=$RPM_OPT_FLAGS" \
	"CDEFS.net="'$(CDEFS.udp)' x11 sndserver
cp -pf "linux-heretic-%{version}/doc/End User License Heretic Source Code.txt" \
	linux-heretic-%{version}/doc/End-User-License-Heretic-Source-Code.txt

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
chmod go= $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/{X11R6/bin,libexec/heretic,share/heretic}
install -m 755 -s linux-heretic-%{version}/xheretic \
	$RPM_BUILD_ROOT/usr/X11R6/bin/xheretic
install -m 755 -s linux-heretic-%{version}/sndserver \
	$RPM_BUILD_ROOT/usr/libexec/heretic/sndserver
cp -pf heretic-1.2/heretic1.wad $RPM_BUILD_ROOT%{_datadir}/heretic/heretic1.wad

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr (644,root,root,755)
%doc heretic-1.2/file_id.diz heretic-1.2/helpme.txt heretic-1.2/license.doc
%doc heretic-1.2/readme.txt
%doc linux-heretic-%{version}/doc/AUTHORS
%doc linux-heretic-%{version}/doc/Changelog
%doc linux-heretic-%{version}/doc/End-User-License-Heretic-Source-Code.txt
%doc linux-heretic-%{version}/doc/README.txt
%doc linux-heretic-%{version}/doc/SourceReadme.txt

%attr (755,root,root) /usr/X11R6/bin/xheretic

%attr (755,root,root,755) /usr/libexec/heretic
%{_datadir}/heretic
