%define		_beta	beta2
%define		_rel	0.5
Summary:	High Performance Content Management
Summary(pl.UTF-8):	System zarządzania treścią o dużej wydajności
Name:		papaya
Version:	5.0.0
Release:	%{_beta}.%{_rel}
License:	GPL
Group:		Applications/WWW
Source0:	http://www.papaya-cms.com/%{name}_installation.download.0776990dd000f86376a804d7b5d6f5ba.zip
# Source0-md5:	2dc8115b4a0befe2cb280967d11fe964
Patch0:		%{name}-webapps.patch
URL:		http://www.papaya-cms.com/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	apache(mod_rewrite)
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Papaya CMS is Open Source Content Management System.

%description -l de.UTF-8
papaya CMS ist ein Open Source Content Management System. Frei von
Lizenzkosten und festen Bindungen mit Dienstleistern. Das System ist
in jeder Hinsicht schnell, einfach und funktional.

%description -l pl.UTF-8
Papaya CMS to mający otwarte źródła system zarządzania treścią.

%prep
%setup -qc
%patch0 -p1

# undos the source
find '(' -name '*.php' -o -name '*.txt' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

cat > apache.conf <<EOF
Alias /%{name} %{_appdir}/htdocs
<Directory %{_appdir}>
	Allow from all
$(cat files/.htaccess)
</Directory>
EOF

cd files
rm -f papaya-lib/.htaccess
rm -f papaya/.htaccess

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/htdocs}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

cd files
cp -a index.php favicon.ico $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a conf.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
cp -a index.php favicon.ico $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a papaya papaya-lib papaya-data papaya-script $RPM_BUILD_ROOT%{_appdir}
cp -a papaya-themes $RPM_BUILD_ROOT%{_appdir}/htdocs

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base >= 1.3.37-3
%webapp_register apache %{_webapp}

%triggerin -- apache1 < 1.3.37-3, apache1-base >= 1.3.37-3
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%lang(de) %doc readme/liesmich.txt
%doc readme/changelog.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
