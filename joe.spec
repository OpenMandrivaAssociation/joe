%define Werror_cflags %nil

Summary:	Summary An easy to use text editor, supporting syntax highlight and UTF-8
Name:		joe
Version:	4.6
Release:	2
License:	GPLv2+
Group:		Editors
Url:		http://joe-editor.sourceforge.net/
Source0:	https://downloads.sourceforge.net/project/joe-editor/JOE%20sources/joe-%{version}/joe-%{version}.tar.gz
# RPM SPEC mode, originally from Suse's joe
Source1:	spec.jsf
Patch0:		joe-3.7-term.patch
Patch1:		joe-3.5-spec-ftyperc.patch
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
%apply_patches

%build
export CFLAGS="$RPM_OPT_FLAGS -DUSE_LOCALE"
%configure
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
%doc ChangeLog docs/help-system.html
%{_bindir}/*
%dir %{_sysconfdir}/joe
%config(noreplace) %{_sysconfdir}/joe/*
%{_datadir}/%{name}/*
%{_mandir}/man1/*
%lang(ru) %{_mandir}/ru/man1/*
%{_datadir}/applications/*
%{_datadir}/doc/joe/*
