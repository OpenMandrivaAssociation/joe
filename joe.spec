%define Werror_cflags %nil

Summary:	Summary An easy to use text editor, supporting syntax highlight and UTF-8
Name:		joe
Version:	3.7
Release:	9
License:	GPL+
Group:		Editors
Url:		http://joe-editor.sourceforge.net/
Source0:	http://puzzle.dl.sourceforge.net/sourceforge/joe-editor/%{name}-%{version}.tar.bz2
# RPM SPEC mode, originally from Suse's joe
Source1:	spec.jsf
Patch1:		joe-3.7-term.patch
Patch2:		joe-3.5-spec-ftyperc.patch
Patch3:		joe-3.7-segfault-fix.patch
BuildRequires:	pkgconfig(ncurses)

%description
Joe is an easy to use, modeless text editor which would be very
appropriate for novices.  Joe uses the same WordStar keybindings used
in Borland's development environment.

You should install joe if you've used it before and you liked it, or
if you're still deciding what text editor you'd like to use, or if you
have a fondness for WordStar.  If you're just starting out, you should
probably install joe because it is very easy to use.

%prep
%setup -q
%patch1 -p0 -b .gnoterm
%patch2 -p1 -b .spec-ftyperc
%patch3 -p0

%build
export CFLAGS="$RPM_OPT_FLAGS -DUSE_LOCALE"
%configure2_5x
%make

%install
%makeinstall

# XXX: hack to install the manpages, otherwise one goes over the other ...
# (trap for when this ugly thing is no more needed)
[ -d %{buildroot}/%{_mandir}/ru ] && exit 1
rm -rf %{buildroot}/%{_mandir}
pushd man && %makeinstall mandir=%{buildroot}/%{_mandir} && popd
pushd man/ru && %makeinstall mandir=%{buildroot}/%{_mandir}/ru && popd
for dir in %{buildroot}/%{_mandir} %{buildroot}/%{_mandir}/ru; do
  pushd $dir/man1
  for bin in jmacs jpico jstar rjoe; do
    ln -s joe.1 ${bin}.1
  done
  popd
done

cp -p %{SOURCE1} %{buildroot}%{_datadir}/joe/syntax/

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Joe
Comment=%{Summary}
Exec=%{_bindir}/%{name} %f
Icon=editors_section
Terminal=true
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Editors;TextEditor;
EOF

%files
%doc ChangeLog HACKING HINTS LIST NEWS README TODO docs/help-system.html
%{_bindir}/*
%dir %{_sysconfdir}/joe
%config(noreplace) %{_sysconfdir}/joe/*
%{_datadir}/%{name}/*
%{_mandir}/man1/*
%lang(ru) %{_mandir}/ru/man1/*
%{_datadir}/applications/*

%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 3.7-6mdv2011.0
+ Revision: 665830
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.7-5mdv2011.0
+ Revision: 606100
- rebuild

* Mon May 03 2010 Emmanuel Andry <eandry@mandriva.org> 3.7-4mdv2010.1
+ Revision: 541757
- fix possible crash with p3 (should fix #58889)

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 3.7-3mdv2010.1
+ Revision: 520137
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.7-2mdv2010.0
+ Revision: 425465
- rebuild

* Thu Jan 15 2009 JÃ©rÃ´me Soyer <saispo@mandriva.org> 3.7-1mdv2009.1
+ Revision: 329765
- New upstream release

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 3.5-8mdv2009.0
+ Revision: 218439
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat Feb 09 2008 Funda Wang <fwang@mandriva.org> 3.5-8mdv2008.1
+ Revision: 164390
- fix license

* Fri Feb 08 2008 Funda Wang <fwang@mandriva.org> 3.5-7mdv2008.1
+ Revision: 164161
- fix LICENSE, it should be GPLv1+

* Thu Feb 07 2008 Thierry Vignaud <tv@mandriva.org> 3.5-6mdv2008.1
+ Revision: 163540
- drop old menu

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 3.5-5mdv2008.1
+ Revision: 127401
- kill re-definition of %%buildroot on Pixel's request


* Tue Feb 06 2007 Gustavo De Nardin <gustavodn@mandriva.com> 3.5-5mdv2007.0
+ Revision: 116886
- fixed menu description
- fixed desktop file
- small fix to spec mode
- added highlight for strings and Requires() to spec mode
- some improvements to spec mode

* Tue Jan 23 2007 Gustavo De Nardin <gustavodn@mandriva.com> 3.5-4mdv2007.1
+ Revision: 112192
- added RPM SPEC mode, from Suse (spec.jsf)
- removed dead patch (joe-3.3-ret.patch.bz2)
- don't package docs in /etc! (as non-docs even)
- manpages for all joe names

* Mon Jan 22 2007 Gustavo De Nardin <gustavodn@mandriva.com> 3.5-3mdv2007.1
+ Revision: 111958
- note about syntax hilight and UTF-8 support on summary
- added docs and russian manpage to package

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.5-2mdv2007.0
- Rebuild

* Wed Aug 09 2006 Giuseppe Ghibò <ghibo@mandriva.com> 3.5-1mdv2007.0
- Release: 3.5
- Rebuilt Patch1.
- Disable Patch2.
- XDG menu.

* Sat Sep 10 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.3-2mdk
- menudir

* Mon Jul 11 2005 Giuseppe Ghibò <ghibo@mandriva.com> 3.3-1mdk
- Release: 3.3.
- Removed old Patch2.
- Merged Patch2 from RH.

* Sun Oct 10 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.1-5mdk
- Added Patch2, to fix documentation/mandirs according to new /etc/joe path
  (from RH).

* Sat Oct 09 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.1-4mdk
- Use /etc/joe and not /etc/joe/joe as config dir (fix bug #12021).

* Tue Aug 17 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 3.1-3mdk
- Rebuild with new menu.

* Tue Jul 20 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.1-2mdk
- Rebuilt.

* Tue Jun 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.1-1mdk
- Release 3.1.

* Tue Apr 27 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.0-1mdk
- Release: 3.1.
- Removed Patch0.

* Sat Feb 07 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.8-2mdk
- Merged gnome term patches from RH (Patch1).
- Renamed Patch2 -> Patch0.

