Name:           inkscape
Version:        0.44.1
Release:        1%{?dist}
Summary:        Vector-based drawing program using SVG

Group:          Applications/Productivity
License:        GPL
URL:            http://inkscape.sourceforge.net/
Source0:        http://download.sourceforge.net/inkscape/inkscape-%{version}.tar.gz
Patch0:         inkscape-0.44.1-incl.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  atk-devel
BuildRequires:  desktop-file-utils
BuildRequires:  freetype-devel
BuildRequires:  gc-devel >= 6.4
BuildRequires:  gettext
BuildRequires:  gtkmm24-devel
BuildRequires:  gtkspell-devel
BuildRequires:  libart_lgpl-devel >= 2.3.10
BuildRequires:  libgnomeprintui22-devel >= 2.2.0
BuildRequires:  gnome-vfs2-devel >= 2.0
BuildRequires:  libpng-devel >= 1.2
BuildRequires:  libsigc++20-devel
BuildRequires:  libxml2-devel >= 2.4.24
BuildRequires:  libxslt-devel
BuildRequires:  pango-devel
BuildRequires:  pkgconfig
BuildRequires:	lcms-devel >= 1.13

Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

Provides:       perl(SpSVG)
Provides:       perl(SVG)


%description
Inkscape is a vector-based drawing program, like CorelDraw® or Adobe
Illustrator® from the proprietary software world, and Sketch or Karbon14 from
the free software world. It is free software, distributed under the terms of
the Gnu General Public License, Version 2.

Inkscape uses W3C SVG as its native file format. It is therefore a very useful
tool for web designers and as an interchange format for desktop publishing.

It has a relatively modern display engine, giving you finely antialiased
display, alpha transparencies, vector fonts and so on. Inkscape is written in
C and C++, using the Gtk+ toolkit and optionally some Gnome libraries.


%prep
%setup -q
%patch0 -p1 -b .incl


%build
%configure                     \
--disable-dependency-tracking  \
--with-xinerama                \
--enable-static=no             \
--with-gnome-vfs               \
--with-inkjar                  \
--enable-lcms

make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}
%find_lang %{name}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install --vendor fedora --delete-original     \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications          \
  --add-category X-Fedora                                  \
  ${RPM_BUILD_ROOT}/usr/share/applications/%{name}.desktop


%clean
rm -rf ${RPM_BUILD_ROOT}


%post
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :


%postun
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc %{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_mandir}/fr/man1/*


%changelog
* Thu Dec 13 2007 Denis Leroy <denis@poolshark.org> - 0.44.1
- Upgrade to 0.44.1
- Merging in spec file from FC-4, with some simplifications

* Sat Dec 17 2005 Denis Leroy <denis@poolshark.org> - 0.43-1
- Update to 0.43
- Remove obsolete x86_64 patch

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
- add %{release} to provides perl(SpSVG) = %{epoch}:%{version}:%{release} only
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.4
- add %{release} to provides
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
