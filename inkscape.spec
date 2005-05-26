Name:           inkscape
Version:        0.41
Release: 4

Summary:        A vector-based drawing program using SVG.

Group:          Applications/Productivity
License:        GPL
URL:            http://inkscape.sourceforge.net/
Source0:        http://download.sourceforge.net/inkscape/inkscape-0.41.tar.bz2
Patch0: inkscape-gcc4.patch
Patch1: inkscape-0.41-64bit.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  atk-devel
BuildRequires:  desktop-file-utils
BuildRequires:  freetype-devel
BuildRequires:  gc-devel
BuildRequires:  gettext
BuildRequires:  gtkmm24-devel
BuildRequires:  libart_lgpl-devel >= 2.3.10
BuildRequires:  libgnomeprintui22-devel >= 2.2.0
BuildRequires:  libpng-devel
BuildRequires:  libsigc++20-devel
BuildRequires:  libxml2-devel >= 2.4.24
BuildRequires:  libxslt-devel
BuildRequires:  pango-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  pkgconfig
BuildRequires:  python-devel
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
%patch0 -p1 -b .gcc4
%patch1 -p1 -b .64bit

%build
aclocal ; autoconf
%configure                     \
--disable-dependency-tracking  \
--with-xinerama                \
--enable-static=no             \
--with-python                  \
--with-inkjar
#temporarily disabled until I can look into it further
#--with-gnome-print             \

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
%doc AUTHORS COPYING ChangeLog NEWS README HACKING
%doc %{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_libdir}/inkscape/


%changelog
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
