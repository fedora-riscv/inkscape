# Preserve lot of debugging information for now. This effectively
# disables FORTIFY_SOURCE, so it must be enabled before Gold
%define optflags %(rpm --eval %%optflags |sed 's/-O2/-O0/')

Name:           inkscape
Version:        0.47
Release:        0.6.20090301svn%{?dist}
Summary:        Vector-based drawing program using SVG

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://inkscape.sourceforge.net/
#Source0:        http://download.sourceforge.net/inkscape/%{name}-%{version}.tar.bz2
# svn export -r20798 https://inkscape.svn.sourceforge.net/svnroot/inkscape/inkscape/trunk@20798 inkscape
# tar cf - inkscape |lzma -9 -c >inkscape.tar.lzma
# Chuck the SVN snapshot specific blocks when bumping to a release:
# perl -e 'while (<>) {/^# BEGIN SVN/ .. /^# END SVN/ or print}' <inkscape.spec
Source0:        %{name}.tar.lzma

Patch0:         inkscape-0.46+devel-uniconv.patch
Patch1:         inkscape-20090227svn-gcc44.patch
Patch2:         inkscape-20090226svn-oldcairo.patch
# BEGIN SVN SNAPSHOT SPECIFIC
Patch3:         inkscape-20090227svn-automake.patch
# END SVN SNAPSHOT SPECIFIC

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  atk-devel
BuildRequires:  desktop-file-utils
BuildRequires:  freetype-devel
BuildRequires:  gc-devel >= 6.4
BuildRequires:  gettext
BuildRequires:  gtkmm24-devel >= 2.8.0
BuildRequires:  gtkspell-devel
BuildRequires:  gnome-vfs2-devel >= 2.0
BuildRequires:  libpng-devel >= 1.2
BuildRequires:  libxml2-devel >= 2.6.11
BuildRequires:  libxslt-devel >= 1.0.15
BuildRequires:  pango-devel
BuildRequires:  pkgconfig
BuildRequires:  lcms-devel >= 1.13
BuildRequires:  cairo-devel
BuildRequires:  dos2unix
BuildRequires:  python-devel
BuildRequires:  poppler-devel
BuildRequires:  loudmouth-devel
BuildRequires:  boost-devel
BuildRequires:  gsl-devel
BuildRequires:  libwpg-devel
BuildRequires:  ImageMagick-c++-devel
BuildRequires:  perl(XML::Parser)
BuildRequires:  perl(ExtUtils::Embed)
BuildRequires:  intltool
# A packaging bug in EL-5
%if 0%{?fedora > 6}
BuildRequires:  popt-devel
%else
BuildRequires:  popt
%endif
# BEGIN SVN SNAPSHOT SPECIFIC
BuildRequires:  autoconf
BuildRequires:  automake
# END SVN SNAPSHOT SPECIFIC

# Incompatible license
BuildConflicts: openssl-devel

# Disable all for now. TODO: Be smarter
%if 0
Requires:       dia
Requires:       pstoedit
Requires:       ghostscript
Requires:       perl(Image::Magick)
Requires:       tex(latex)
Requires:       tex(dvips)
Requires:       transfig
Requires:       gimp
Requires:       numpy
Requires:       python-lxml
Requires:       uniconvertor
# TODO: Deal with these (autoreqs, disabled now):
# perl(Cwd)
# perl(Exporter)
# perl(File::Basename)
# perl(Getopt::Long)
# perl(Getopt::Std)
# perl(MIME::Base64)
# perl(Pod::Usage)
# perl(SVG)
# perl(SVG::Parser)
# perl(XML::XQL)
# perl(XML::XQL::DOM)
# perl(strict)
# perl(vars)
# perl(warnings)
%endif

Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

# Filter out perl requires and provides
# XXX: For now _all_
%global __perl_provides %{nil}
%global __perl_requires %{nil}

%description
Inkscape is a vector graphics editor, with capabilities similar to
Illustrator, CorelDraw, or Xara X, using the W3C standard Scalable Vector
Graphics (SVG) file format.  It is therefore a very useful tool for web
designers and as an interchange format for desktop publishing.

Inkscape supports many advanced SVG features (markers, clones, alpha
blending, etc.) and great care is taken in designing a streamlined
interface. It is very easy to edit nodes, perform complex path operations,
trace bitmaps and much more.


%package view
Summary:        Viewing program for SVG files
Group:          Applications/Productivity

%description view
Viewer for files in W3C standard Scalable Vector Graphics (SVG) file
format.


%package docs
Summary:        Documentation for Inkscape
Group:          Documentation

%description docs
Tutorial and examples for Inkscape, a graphics editor for vector
graphics in W3C standard Scalable Vector Graphics (SVG) file format.


%prep
%setup -q -n %{name}
%patch0 -p1 -b .uniconv
%patch1 -p1 -b .gcc44
%patch2 -p0 -b .oldcairo
# BEGIN SVN SNAPSHOT SPECIFIC
%patch3 -p0 -b .automake
# END SVN SNAPSHOT SPECIFIC

# https://bugs.launchpad.net/inkscape/+bug/314381
# A couple of files have executable bits set,
# despite not being executable
(find . \( -name '*.cpp' -o -name '*.h' \) -perm +111
	find share/extensions -name '*.py' -perm +111
) |xargs chmod -x

# Fix end of line encodings
dos2unix -k -q share/extensions/*.py


%build
# BEGIN SVN SNAPSHOT SPECIFIC
sh autogen.sh
# END SVN SNAPSHOT SPECIFIC
%configure                      \
        --with-python           \
        --with-perl             \
        --with-gnome-vfs        \
        --with-xft              \
        --enable-lcms           \
        --enable-poppler-cairo  \
        --disable-dependency-tracking
#        --enable-inkboard       \

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install --vendor fedora --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

# No skencil anymore
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions/sk2svg.sh

%find_lang %{name}


%check
# XXX: Tests fail, ignore it for now
make -k check || :


%clean
rm -rf $RPM_BUILD_ROOT


%post
exec >/dev/null 2>&1
update-desktop-database %{_datadir}/applications || :
touch --no-create %{_datadir}/icons/hicolor
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%postun
exec >/dev/null 2>&1
update-desktop-database %{_datadir}/applications || :
touch --no-create %{_datadir}/icons/hicolor
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/inkscape
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/clipart
%{_datadir}/inkscape/extensions
%{_datadir}/inkscape/filters
%{_datadir}/inkscape/fonts
%{_datadir}/inkscape/gradients
%{_datadir}/inkscape/icons
%{_datadir}/inkscape/keys
%{_datadir}/inkscape/markers
%{_datadir}/inkscape/palettes
%{_datadir}/inkscape/patterns
%{_datadir}/inkscape/screens
%{_datadir}/inkscape/templates
%{_datadir}/inkscape/ui
%{_datadir}/applications/fedora-inkscape.desktop
%{_datadir}/icons/hicolor/scalable/apps/inkscape.svg
%{_datadir}/pixmaps/inkscape.png
%{_mandir}/man1/inkscape.1*
%{_mandir}/man1/inkview.1*
%{_mandir}/fr/man1/inkscape.1*


%files view
%defattr(-,root,root,-)
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/tutorials
%{_datadir}/inkscape/examples
%doc AUTHORS COPYING ChangeLog NEWS README


%files docs
%defattr(-,root,root,-)
%{_bindir}/inkview
%doc AUTHORS COPYING ChangeLog NEWS README


%changelog
* Wed Mar 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.6.20090301svn
- Rebuild for new ImageMagick

* Wed Mar 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.5.20090301svn
- Split documentation and inkview into subpackages

* Mon Mar 02 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.4.20090301svn
- Bump to later SVN snapshot to fix inkscape/+bug/331864
- Fix a startup crash when compiled with GCC 4.4
- It even runs now! :)

* Fri Feb 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.4.20090227svn
- Enable the test suite

* Fri Feb 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.3.20090227svn
- Past midnight! :)
- More recent snapshot, our gcc44 fixes now upstream
- One more gcc44 fix, it even compiles now
- We install icons now, update icon cache
- Disable inkboard, for it won't currently compile

* Thu Feb 26 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.3.20090226svn
- Later snapshot
- Compile with GCC 4.4

* Tue Jan 06 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.3.20090105svn
- Update to newer SVN
- Drop upstreamed patches
- Enable WordPerfect Graphics support
- Enable embedded Perl scripting
- Enable Imagemagick support
- Disable OpenSSL due to licensing issues

* Thu Aug 14 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.3.20080814svn
- Update to today's SVN snapshot
- Drop the upstreamed poppler patch

* Wed Aug 13 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.2.20080705svn
- Rediff patches for zero fuzz
- Use uniconvertor to handle CDR and WMF (#458845)

* Wed Jul 09 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.1.20080705svn
- Subversion snapshot

* Wed Jul 09 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.46-4
- Fix compile issues with newer gtk and poppler

* Thu Jun 26 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.46-3
- Remove useless old hack, that triggered an assert after gtkfilechooser switched to gio

* Fri Apr 11 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-2.1
- More buildrequires more flexible, so that this builds on RHEL

* Sat Apr 05 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-2
- Fix LaTeX rendering, #441017

* Tue Mar 25 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-1
- 0.46 released

* Sun Mar 23 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.3.pre3
- Rebuild for newer Poppler

* Wed Mar 12 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.2.pre3
- Probably last prerelease?

* Fri Feb 22 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.2.pre2
- Panel icon sizes

* Sun Feb 17 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.1.pre2
- 0.46pre2
- Dropping upstreamed patches

* Sat Feb 16 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-5
- Attempt to fix the font selector (#432892)

* Thu Feb 14 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-4
- Tolerate recoverable errors in OCAL feeds
- Fix OCAL insecure temporary file usage (#432807)

* Wed Feb 13 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-3
- Fix crash when adding text objects (#432220)

* Thu Feb 07 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-2
- Build with gcc-4.3

* Wed Feb 06 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-1
- 0.46 prerelease
- Minor cosmetic changes to satisfy the QA script
- Dependency on Boost
- Inkboard is not optional
- Merge from Denis Leroy's svn16571 snapshot:
- Require specific gtkmm24-devel versions
- enable-poppler-cairo
- No longer BuildRequire libsigc++20-devel

* Wed Dec  5 2007 Denis Leroy <denis@poolshark.org> - 0.45.1-5
- Rebuild with new openssl

* Sun Dec 02 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-4
- Added missing dependencies for modules (#301881)

* Sun Dec 02 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-3
- Satisfy desktop-file-validate, so that Rawhide build won't break

* Sat Dec 01 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-2
- Use GTK print dialog
- Added compressed SVG association (#245413)
- popt headers went into popt-devel, post Fedora 7
- Fix macro usage in changelog

* Wed Mar 21 2007 Denis Leroy <denis@poolshark.org> - 0.45.1-1
- Update to bugfix release 0.45.1
- Added R to ImageMagick-perl (#231563)

* Wed Feb  7 2007 Denis Leroy <denis@poolshark.org> - 0.45-1
- Update to 0.45
- Enabled inkboard, perl and python extensions
- Added patch for correct python autodetection
- LaTex patch integrated upstreamed, removed
- Some rpmlint cleanups

* Wed Dec  6 2006 Denis Leroy <denis@poolshark.org> - 0.44.1-2
- Added patches to fix LaTex import (#217699)
- Added patch to base postscript import on pstoedit plot-svg

* Thu Sep  7 2006 Denis Leroy <denis@poolshark.org> - 0.44.1-1
- Update to 0.44.1
- Removed png export patch, integrated upstream
- Some updated BRs

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 0.44-6
- FE6 Rebuild

* Tue Aug 22 2006 Denis Leroy <denis@poolshark.org> - 0.44-5
- Removed skencil Require (bug 203229)

* Thu Aug 10 2006 Denis Leroy <denis@poolshark.org> - 0.44-4
- Added patch to fix png dpi export problem (#168406)

* Wed Aug  9 2006 Denis Leroy <denis@poolshark.org> - 0.44-3
- Bumping up release to fix upgrade path

* Wed Jun 28 2006 Denis Leroy <denis@poolshark.org> - 0.44-2
- Update to 0.44
- Removed obsolete patches
- Disabled experimental perl and python extensions
- Added pstoedit, skencil, gtkspell and LittleCms support
- Inkboard feature disabled pending further security tests

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 0.43-3
- Rebuild

* Mon Jan 16 2006 Denis Leroy <denis@poolshark.org> - 0.43-2
- Updated GC patch, bug 171791

* Sat Dec 17 2005 Denis Leroy <denis@poolshark.org> - 0.43-1
- Update to 0.43
- Added 2 patches to fix g++ 4.1 compilation issues
- Enabled new jabber/loudmouth-based inkboard feature

* Mon Sep 26 2005 Denis Leroy <denis@poolshark.org> - 0.42.2-2
- rebuilt with newer glibmm

* Thu Sep  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42.2-1
- update to 0.42.2

* Thu Aug 18 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-3
- rebuilt
- add patch to repair link-check of GC >= 6.5 (needs pthread and dl)

* Fri Jul 29 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-2
- Extend ngettext/dgettext patch for x86_64 build.

* Tue Jul 26 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-1
- update to 0.42 (also fixes #160326)
- BR gnome-vfs2-devel
- no files left in %%_libdir/inkscape
- include French manual page
- GCC4 patch obsolete, 64-bit patch obsolete, dgettext patch split off

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-7
- append another 64-bit related patch (dgettext configure check failed)

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-6
- remove explicit aclocal/autoconf calls in %%build as they create a
  bad Makefile for FC4/i386, which causes build to fail (#156228),
  and no comment explains where they were added/needed

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-5
- bump and rebuild as 0.41-4 failed in build system setup

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.41-4
- add patch for gcc4 problems (ignacio, #156228)
- fix build on 64bit boxes.  sizeof(int) != sizeof(void*)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.41-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Feb 09 2005 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.41-1
- 0.41.
- enable python.

* Sat Dec 04 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.40-1
- 0.40.

* Mon Nov 16 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.40-0.pre3
- 0.40pre3.

* Thu Nov 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.39-0.fdr.2
- post/postun for new mime system.
- Dropped redundant BR XFree86-devel.

* Sun Aug 29 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.39-0.fdr.1
- 0.39.

* Fri Apr 10 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.1-0.fdr.1
- respin real fix for Provides/Requires for perl(SpSVG)

* Fri Apr 9 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.1-0.fdr.0
- respin with updated tarball with fix for postscript printing

* Thu Apr 8 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38-0.fdr.2
- respin to fix provides

* Thu Apr 8 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.0.fdr.1
- version upgrade with many improvements and bug fixes

* Fri Mar 19 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.7
- repsin - sourceforge does not allow reloading files with same name
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.6
- fix typo in provides
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.5
- add %%{release} to provides perl(SpSVG) = %%{epoch}:%%{version}:%%{release} only
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.4
- add %%{release} to provides
* Sun Mar 14 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.3
- add arch dependent flags
* Thu Mar 11 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.2
- add libsigc++-devel instead of add libsigc++ - duh
- add BuildRequires:  perl-XML-Parser
- fix package name to follow package naming guidelines
* Mon Mar 1 2004   P Linnell <scribusdocs at atlantictechsolutions.com>   0:0.37.1.fdr.1
- disable static libs
- enable inkjar
* Tue Feb 10  2004 P Linnell <scribusdocs at atlantictechsolutions.com>   0:0.37.0.fdr.1
- pgp'd tarball from inkscape.org
- clean out the cvs tweaks in spec file
- enable gnome-print
- add the new tutorial files
- make sure .mo file gets packaged
- add provides: perlSVG
- submit to Fedora QA
* Sat Feb 7  2004 P Linnell <scribusdocs at atlantictechsolutions.com>
- rebuild of current cvs
- tweaks to build cvs instead of dist tarball
- add inkview
* Sat Dec 20 2003 P Linnell <scribusdocs at atlantictechsolutions.com>
- First crack at Fedora/RH spec file
- nuke gnome print - it won't work (bug is filed already)
