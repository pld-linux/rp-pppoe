Summary:	PPP Over Ethernet client
Summary(pl):	Klient PPP Poprzez Ethernet (PPPoE)
Name:		rp-pppoe
Version:	3.5
Release:	1
Source0:	http://www.roaringpenguin.com/pppoe/%{name}-%{version}.tar.gz
URL:		http://www.roaringpenguin.com/pppoe/
License:	GPL
Group:		Networking
Requires:	ppp >= 2.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. Roaring Penguin has a free
client for Linux systems to connect to PPPoE service providers.

The client is a user-mode program and does not require any kernel
modifications. It is fully compliant with RFC 2516, the official PPPoE
specification.

%description -l pl
PPPoE (Protokó³ Punkt-Punkt poprzez Ethernet) jest protoko³em
u¿ywanym przez wielu dostarczycieli us³ugi ADSL. 

Klient jest programem dzia³aj±cym w przestrzeni u¿ytkownika,
a to oznacza, ¿e nie wymaga modyfikacji kernela. Jest w pe³ni
zgodny z oficjaln± specyfikacj± PPPoE - RFC 2516.

%package gui
Summary:	GUI front-end for rp-pppoe
Summary(pl):	Graficzny interfejs dla rp-pppoe
Group:		X11/Networking
Requires:	rp-pppoe >= 3.4

%description gui
This package contains the graphical frontend (tk-based) for rp-pppoe.

%description -l pl gui
Graficzny interfejs u¿ytkownika (bazuj±cy na tk) dla rp-pppoe.

%prep
%setup -q
%build
cd src
%{__aclocal}
%{__autoconf}
%configure
# kernel mode PPPoE support is in pppd 2.4.2 (cvs) package
# and we want here such support in utilities like pppoe-server
echo '#define HAVE_LINUX_KERNEL_PPPOE 1' >> config.h
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	RPM_INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C gui install \
	RPM_INSTALL_ROOT=$RPM_BUILD_ROOT

# This is necessary for the gui to work, but it shouldn't be done here !
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ppp/rp-pppoe-gui

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* README
%attr(755,root,root) %{_sbindir}/*
%exclude %{_bindir}/tkpppoe
%exclude %{_sbindir}/pppoe-wrapper

%config(noreplace) %{_sysconfdir}/ppp/pppoe.conf
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%config(noreplace) %{_sysconfdir}/ppp/firewall-masq
%config(noreplace) %{_sysconfdir}/ppp/firewall-standalone
%{_mandir}/man[58]/*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tkpppoe
%attr(755,root,root) %{_sbindir}/pppoe-wrapper
%dir %{_sysconfdir}/ppp/rp-pppoe-gui
%{_datadir}/tkpppoe
%{_mandir}/man1/*
