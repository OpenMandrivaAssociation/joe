%define		Summary An easy to use text editor, supporting syntax highlight and UTF-8
Summary:	%Summary
Name:		joe
Version:	3.5
Release:	%mkrel 5
License:	GPL
Group:		Editors
Source:		http://puzzle.dl.sourceforge.net/sourceforge/joe-editor/%{name}-%{version}.tar.bz2
# RPM SPEC mode, originally from Suse's joe
Source1:	spec.jsf
Patch1:		joe-3.5-term.patch
Patch2:		joe-3.5-spec-ftyperc.patch
Url:		http://joe-editor.sourceforge.net/
BuildRequires:	ncurses-devel

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
%patch1 -p1 -b .gnoterm
%patch2 -p1 -b .spec-ftyperc

%build
export CFLAGS="$RPM_OPT_FLAGS -DUSE_LOCALE"
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
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

cp -p %{SOURCE1} %{buildroot}%{_sysconfdir}/joe/syntax/

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):\
	needs="text"\
	section="More Applications/Editors"\
	title="Joe"\
	longtitle="Joe - a text ANSI editor"\
	command="%{_bindir}/joe"\
%if %{mdkversion} >= 200610
	xdg="true" \
%endif
	icon="editors_section.png"
EOF

%if %{mdkversion} >= 200610
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Joe
Comment=%{Summary}
Exec=%{_bindir}/%{name} %f
Icon=editors_section
Terminal=true
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Editors;TextEditor;
EOF
%endif

%post
%if %{mdkversion} >= 200610
%update_desktop_database
%endif
%update_menus

%postun
%if %{mdkversion} >= 200610
%clean_desktop_database
%endif
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%{_bindir}/*
%dir %{_sysconfdir}/joe 
%config(noreplace) %{_sysconfdir}/joe/*
%{_mandir}/man1/*
%lang(ru) %{_mandir}/ru/man1/*
%{_menudir}/%{name}
%if %{mdkversion} >= 200610
%{_datadir}/applications/*
%endif
# joe's build puts docs here(!), and leaves out some interesting files...
%exclude %{_sysconfdir}/joe/doc
%doc ChangeLog HACKING HINTS LIST NEWS README TODO docs/help-system.html


