%define Werror_cflags %nil

%define		Summary An easy to use text editor, supporting syntax highlight and UTF-8
Summary:	%Summary
Name:		joe
Version:	3.7
Release:	%mkrel 3
License:	GPL+
Group:		Editors
Source:		http://puzzle.dl.sourceforge.net/sourceforge/joe-editor/%{name}-%{version}.tar.bz2
# RPM SPEC mode, originally from Suse's joe
Source1:	spec.jsf
Patch1:		joe-3.7-term.patch
Patch2:		joe-3.5-spec-ftyperc.patch
Url:		http://joe-editor.sourceforge.net/
BuildRequires:	ncurses-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

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

cp -p %{SOURCE1} %{buildroot}%{_datadir}/joe/syntax/


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
%if %mdkversion < 200900
%update_desktop_database
%endif
%endif
%if %mdkversion < 200900
%update_menus
%endif

%postun
%if %{mdkversion} >= 200610
%if %mdkversion < 200900
%clean_desktop_database
%endif
%endif
%if %mdkversion < 200900
%clean_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%{_bindir}/*
%dir %{_sysconfdir}/joe
%config(noreplace) %{_sysconfdir}/joe/*
%{_datadir}/%{name}/*
%{_mandir}/man1/*
%lang(ru) %{_mandir}/ru/man1/*
%if %{mdkversion} >= 200610
%{_datadir}/applications/*
%endif
%doc ChangeLog HACKING HINTS LIST NEWS README TODO docs/help-system.html
