Summary: Heretic for the X Window System
Name: heretic
Version: 0.9.5
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
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Heretic is a supernatural blast-fest that is the most realistic,
action-packed fantasy combat computer game for the PC.  Created
by the graphic masters at Raven Software in concert with the
technical gurus of id Software, Heretic adds new levels of play
and graphic wonder to the tried and true DOOM gaming environment.

%changelog
* Mon Feb 15 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- updated to heretic 0.9.5
- removed the UDP networking patch as no longer necessary
- updated the Alpha patch
- removed the geometry patch as already applied
- removed the namespace patch as already applied
- updated the paths patches

* Thu Feb 11 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- added an Alpha patch based on works by Robert Bowles

* Sat Feb  6 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- removed unnecessary libm reference
- fixed window's geometry handling

* Thu Feb  4 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- updated to heretic 0.9.3
- removed the P_NewChaseDir patch as no longer necessary
- updated the UDP networking patch
- updated the glibc 2.1 patch
- updated the file paths patch to support HERETICHOME

* Tue Feb  2 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- fixed the glibc 2.1 patch to be glibc 2.0 clean
- fixed remaining known bugs in UDP networking

* Mon Feb  1 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- updated to heretic 0.9.3alpha
- added a patch for UDP networking

* Fri Jan 29 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- added a fix to P_NewChaseDir to stop enemies being randomly
  thrown out of the legal area of the game map
- disabled some debugging facilities

* Mon Jan 25 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- updated to heretic 0.9.2
- removed the patch for P_FindNextHighestFloor as the problem is
  fixed in this version

* Sun Jan 24 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- added a fix for a nasty buffer overflow in P_FindNextHighestFloor
  (whoever wrote the function must have been drunk or crazy...)

* Fri Jan 22 1999 Maciej W. Rozycki <macro@ds2.pg.gda.pl>
- initial build for heretic 0.9.1.1

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
