%bcond_with gtk3

Name:           gxine
Version:        0.5.910
Release:        3%{?dist}
Summary:        GTK frontend for the xine multimedia library
License:        GPLv2+
URL:            http://www.xine-project.org/home
Source0:        http://downloads.sourceforge.net/xine/%{name}-%{version}.tar.xz

Patch1:         gxine-0.5.902-non-separate-toolbar.patch
# some multilib issues
Patch3:         gxine-0.5.907-lirc.patch

BuildRequires:  gcc
BuildRequires:  js-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
%if %{with gtk3}
BuildRequires:  gtk3-devel
%else
BuildRequires:  gtk2-devel
%endif
Buildrequires:  xine-lib-devel

# for dbus support
BuildRequires:  dbus-glib-devel
# for gudev support (device detection)
BuildRequires:  libgudev1-devel
# for LIRC support
BuildRequires:  lirc-devel
# for XTest support
BuildRequires:  libXtst-devel
# for mozplugin
BuildRequires:  libXaw-devel
BuildRequires:  nspr-devel

# for linkage patch
BuildRequires:  libtool


%description
gxine is a fully-featured free audio/video player for unix-like systems which
uses libxine for audio/video decoding and playback. For more information on
what formats are supported, please refer to the libxine documentation.
gxine is a gtk based gui for this xine-library alternate to xine-ui.


%package mozplugin
Summary:  Mozilla plugin for gxine
Requires: %{name} = %{version}-%{release}
Requires: mozilla-filesystem

%description mozplugin
This plugin allows gxine to be embedded in a web browser.


%prep
%setup -q
%patch1 -p1 -b .non-separate-toolbar
%patch3 -p1 -b .lirc

%{__sed} -i 's/Name=gxine/Name=GXine/' gxine.desktop.in
autoreconf -if


%build
%configure --with-dbus --with-logo-format=image --with-gudev \
  --with-browser-plugin --disable-integration-wizard         \
  --enable-watchdog  --disable-own-playlist-parsers          \
  --disable-deprecated \
%if %{with gtk3}
  --with-gtk3
%endif

make %{?_smp_mflags}


%install
%make_install

# Remove .las
%{__rm} %{buildroot}%{_libdir}/gxine/*.la

# Move Mozilla plugin
mkdir -p %{buildroot}%{_libdir}/mozilla/plugins/
mv %{buildroot}%{_libdir}/gxine/gxineplugin.so %{buildroot}%{_libdir}/mozilla/plugins/

%find_lang %{name} --all-name

desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications             \
  --mode 0644                                            \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog README TODO
%dir %{_sysconfdir}/gxine/
%config(noreplace) %{_sysconfdir}/gxine/gtk.css
%config(noreplace) %{_sysconfdir}/gxine/gtkrc
%config(noreplace) %{_sysconfdir}/gxine/keypad.xml
%config(noreplace) %{_sysconfdir}/gxine/startup
%config(noreplace) %{_sysconfdir}/gxine/toolbar*.xml
%{_bindir}/gxine*
%{_mandir}/man1/gxine*.1*
%lang(de) %{_mandir}/de/man1/gxine*.1*
%lang(es) %{_mandir}/es/man1/gxine*.1*
%{_datadir}/gxine/
%{_datadir}/pixmaps/gxine.png
%{_datadir}/icons/*/*/apps/gxine.png
%{_datadir}/applications/*gxine.desktop

%files mozplugin
%license COPYING
%{_libdir}/mozilla/plugins/gxineplugin.so


%changelog
* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.5.910-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 20 2018 Xavier Bachelot <xavier@bachelot.org> - 0.5.910-3
- Add BR: gcc.
- Add conditional for building against GTK3.

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.5.910-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 31 2017 Xavier Bachelot <xavier@bachelot.org> - 0.5.910-1
- Update to 0.5.910.
- Specfile cleanup.

* Mon Dec 18 2017 Xavier Bachelot <xavier@bachelot.org> - 0.5.909-1
- Update to 0.5.909.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.5.908-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.5.908-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.5.908-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Xavier Bachelot <xavier@bachelot.org> - 0.5.908-1
- Update to 0.5.908.

* Wed Oct 23 2013 Xavier Bachelot <xavier@bachelot.org> - 0.5.907-11
- Rebuild for xine-lib 1.2.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.907-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 24 2013 Jon Ciesla <limburgher@gmail.com> - 0.5.907-9
- Drop desktop vendor tag.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.907-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Martin Sourada <mso@fedoraproject.org> - 0.5.907-7
- Switch build to mozjs185, hopefully it has more stable API
- SPEC clean-up

* Fri Aug 10 2012 Martin Sourada <mso@fedoraproject.org> - 0.5.907-6
- Fix build

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.907-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 02 2012 Martin Sourada <mso@fedoraproject.org> - 0.5.907-4
- Fix directories ownership -- on EPEL own 
   %%{_libdir}/mozilla/plugins, on Fedora require mozilla-filesystem

* Fri Mar 02 2012 Martin Sourada <mso@fedoraproject.org> - 0.5.907-3
- Fix build on EPEL, switch to gecko-devel

* Thu Feb 23 2012 Martin Sourada <mso@fedoraproject.org> - 0.5.907-2
- Try to fix build with newer glibc

* Wed Feb 22 2012 Martin Sourada <mso@fedoraproject.org> - 0.5.907-1
- Update to 0.5.907
- Drop .desktop and JS patches -- fixed upstream.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.905-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 19 2011 Martin Stransky <stransky@redhat.com> - 0.5.905-6
- Added a fix for js 1.8.5

* Wed Feb 09 2011 Martin Sourada <mso@fedoraproject.org> - 0.5.905-5
- Use libjs instead of libmozjs -- gxine does not build against xulrunner-2
- Use gudev instead of HAL for device detection

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.905-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 13 2010 Martin Sourada <mso@fedoraproject.org> - 0.5.905-3
- Fix build on devel
- http://fedoraproject.org/wiki/Features/ChangeInImplicitDSOLinking

* Sun Jan 10 2010 Martin Sourada <mso@fedoraproject.org> - 0.5.905-2
- Fix source URL

* Fri Jan 01 2010 Martin Sourada <mso@fedoraproject.org> - 0.5.905-1
- 0.5.905
- Should fix sigsegv on exit
- Reenable lirc support (detection fixed upstream)

* Sun Oct 25 2009 Martin Sourada <mso@fedoraproject.org> - 0.5.904-1
- 0.5.904
- Disable lirc support (./configure does not find fedora's lirc)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.903-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.903-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jul 19 2008 Martin Sourada <martin.sourada@gmail.com> - 0.5.903-2
- rebuild for new xulrunner
- drop dist checks to keep the spec cleaner
- drop versioned dependency on gecko-libs

* Sun Jun 15 2008 Martin Sourada <martin.sourada@gmail.com> - 0.5.903-1
- new upstream version

* Tue Apr 22 2008 Martin Sourada <martin.sourada@gmail.com> - 0.5.902-1
- new upstream version
- drop xine-lib version patch - fixed in upstream
- drop keep track of window state patch - fixed in upstream
- add BR: hal
- customize configure options
- do not use spearate toolbar by default

* Sat Feb 09 2008 Martin Sourada <martin.sourada@gmail.com> - 0.5.11-17
- add patch to support x.y.z.w version strings in xine-lib

* Fri Feb 08 2008 Martin Sourada <martin.sourada@gmail.com> - 0.5.11-16
- rebuild for gcc 4.3

* Fri Dec 21 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-15
- rebuild for new xulrunner

* Mon Dec 10 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-14
- xulrunner not available on F-8 (use js)
- js and lirc not available on EL-5 (use firefox-js and drop lirc support)

* Mon Dec 10 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-13
- spec cleanup
- prepare for EPEL

* Wed Nov 21 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-12
- --rpath hack hopefully no longer needed
- build against new xulrunner

* Thu Nov 15 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-11
- add --rpath to xulruner dir, so that libmozjs.so loads correctly
- enable xulrunner's libmozjs.so

* Wed Nov 14 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-10
- Add desktop-file-utils BR

* Wed Nov 14 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-9
- Clean up the BRs, prepare for usage of mozjs from xulrunner

* Tue Oct 09 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-8
- Register file handler properly (rhbz #321471)

* Tue Aug 21 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-7
- Rebuild

* Thu Aug 09 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-6
- Update License: field to GPLv2+

* Fri Jul 06 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-5
- Change the name displayed in menu to GXine Video Player

* Wed May 16 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-4
- rebuild to include ppc64 arch

* Sun Mar 25 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-3
- fix rpmlint warning

* Wed Mar 14 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-2
- add patch to keep track of window state (backport from 0.6.0 branch)

* Thu Feb 01 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.11-1
- Bump to new (bugfix) release
- Removed stream end crash patch - fixed in upstream

* Wed Jan 24 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.10-5
- Stream end crash when modal dialog opened patch: see upstream bz #1643093

* Thu Jan 18 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.10-4
- replace R: firefox with R: %%{_libdir}/mozilla/plugins

* Wed Jan 17 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.10-3
- fix BR: gettext instead of gettext-devel
- add R: firefox to mozplugin subpackage

* Thu Jan 11 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.10-2
- fix url
- fix require in mozplugin subpackage
- install desktop file correctly

* Thu Jan 11 2007 Martin Sourada <martin.sourada@seznam.cz> - 0.5.10-1
- Update to upstream release 0.5.10
- Remove screensaver patch (it was approved by upstream)

* Thu Dec 28 2006 Martin Sourada <martin.sourada@seznam.cz> - 0.5.9-2
- Rebuild

* Sun Dec 17 2006 Martin Sourada <martin.sourada@seznam.cz> - 0.5.9-1.1
- Add BR dbus-devel

* Sat Dec 16 2006 Michel Salim <michel.salim@gmail.com> - 0.5.9-1
- Update to upstream release 0.5.9
- Drop logo.ogg, gxine now includes a JPEG logo

* Sat Dec 16 2006 Michel Salim <michel.salim@gmail.com> - 0.5.8-4
- Fix gnome-screensaver DBUS call
- Separate mozplugin subpackage (from Martin Sourada)
- Add missing BuildRequires

* Tue Nov  7 2006 Mola Pahnadayan <mola@c100c.com> - 0.5.8-3
- Add libXinerama-devel , lirc-devel >= 0.8.1 in build requires
- Fix find_lang
ambiguous

* Tue Oct 31 2006 Mola Pahnadayan <mola@c100c.com> - 0.5.8-2
- rm non-free logo
- add patch to install free-logo
- uses %%find_lang

* Tue Oct 31 2006 Mola Pahnadayan <mola@c100c.com> - 0.5.8-1
- Updated to 0.5.8

* Tue Sep 19 2006 Mola Pahnadayan <mola@c100c.com> - 0.5.7-1
- write new spec file
- Updated to release 0.5.7
