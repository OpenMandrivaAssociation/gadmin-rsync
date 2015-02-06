# if I fix the string literal errors according to the wiki Problems
# page, it crashes on startup - AdamW 2009/01
%define Werror_cflags %nil

Summary:	A GTK+ administation tool for rsync
Name:		gadmin-rsync
Version:	0.1.7
Release:	3
License:	GPLv3+
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gadmin-rsync/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
Requires:	rsync
Requires:	usermode-consoleonly

%description
Gadmin-Rsync is a fast and easy to use GTK+ administration tool for rsync.

%prep
%setup -q

%build
%configure2_5x
%make

%install
%makeinstall

install -d %{buildroot}%{_sysconfdir}/%{name}

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

# Mandriva Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e 's,%{name}.png,%{name},g' desktop/%{name}.desktop
sed -i -e 's,GADMIN-RSYNC,Gadmin-Rsync,g' desktop/%{name}.desktop
mv desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Prepare usermode entry
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}

%files
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/%{name}.png



%changelog
* Wed Mar 16 2011 Stéphane Téletchéa <steletch@mandriva.org> 0.1.7-1mdv2011.0
+ Revision: 645176
- update to new version 0.1.7

* Sun Nov 28 2010 Funda Wang <fwang@mandriva.org> 0.1.6-1mdv2011.0
+ Revision: 602227
- update to new version 0.1.6

* Thu Jan 07 2010 Emmanuel Andry <eandry@mandriva.org> 0.1.5-1mdv2010.1
+ Revision: 487291
- New version 0.1.5

* Fri Sep 11 2009 Emmanuel Andry <eandry@mandriva.org> 0.1.4-1mdv2010.0
+ Revision: 438459
- New version 0.1.4

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.1.1-2mdv2010.0
+ Revision: 437643
- rebuild

* Tue Feb 17 2009 Jérôme Soyer <saispo@mandriva.org> 0.1.1-1mdv2009.1
+ Revision: 341535
- New upstream release

* Sun Jan 04 2009 Adam Williamson <awilliamson@mandriva.org> 0.1.0-1mdv2009.1
+ Revision: 324190
- import gadmin-rsync


