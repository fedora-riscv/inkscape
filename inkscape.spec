Name:           inkscape
Version:        0.38.1
Release:        0.fdr.1.1
Epoch:		0
Summary:        A vector-based drawing program using SVG.
Group:          Applications/Productivity
License:        GPL
URL:            http://inkscape.sourceforge.net/
Source0:        http://dl.sf.net/sourceforge/inkscape/inkscape-0.38.1.tar.bz2

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:  XFree86-devel 
BuildRequires:  libgnomeprintui22-devel >= 0:2.2.0
BuildRequires:  libpng-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libart_lgpl-devel >= 0:2.3.10
BuildRequires:  freetype-devel
BuildRequires:  libxml2-devel >= 2-2.4.24
BuildRequires:  gtk2-devel
BuildRequires:  pango-devel
BuildRequires:  atk-devel
BuildRequires:  pkgconfig
BuildRequires:  libsigc++-devel >= 0:1.2.5
BuildRequires:  perl-XML-Parser

Provides:	perl(SpSVG)
Provides:	perl(SVG)


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

%build
 
%configure                     \
--disable-dependency-tracking  \
%ifarch i386
        --disable-mmx          \
%endif
%ifarch i686
        --enable-mmx           \
%endif
%ifarch athlon
        --enable-mmx           \
%endif
--with-gnome-print             \
--with-xinerama \
--enable-static=no \
--with-inkjar

make %{?_smp_mflags}



%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}
%find_lang %{name}


desktop-file-install --vendor fedora --delete-original     \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications          \
  --add-category X-Fedora                                  \
  --add-category Application                               \
  --add-category Graphics                                  \
  ${RPM_BUILD_ROOT}/usr/share/applications/%{name}.desktop


%clean
rm -rf ${RPM_BUILD_ROOT}



%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README HACKING
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/locale/*/LC_MESSAGES/inkscape.mo
%{_datadir}/pixmaps/*
%{_mandir}/man1/*




%changelog
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
