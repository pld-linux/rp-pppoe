Summary:	PPP Over Ethernet client
Summary(pl.UTF-8):	Klient PPP Poprzez Ethernet (PPPoE)
Summary(pt_BR.UTF-8):	Protocolo PPPoE (PPP over Ethernet), usado comumente com modens xDSL
Summary(ru.UTF-8):	PPP Over Ethernet (поддержка xDSL)
Summary(uk.UTF-8):	PPP Over Ethernet (підтримка xDSL)
Name:		rp-pppoe
Version:	3.10
Release:	1
License:	GPL v2+
Group:		Networking
Source0:	http://www.roaringpenguin.com/files/download/%{name}-%{version}.tar.gz
# Source0-md5:	d58a13cc4185bca6121a606ff456dec0
Source1:	%{name}-server.init
Source2:	%{name}-server.sysconfig
Source3:	%{name}-relay.init
Source4:	%{name}-relay.sysconfig
Patch0:		%{name}-ac.patch
Patch1:		%{name}-tkpppoe.in.patch
Patch2:		%{name}-plugins.patch
URL:		http://www.roaringpenguin.com/products/pppoe
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	ppp >= 2.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. Roaring Penguin has a free
client for Linux systems to connect to PPPoE service providers.

The client is a user-mode program and does not require any kernel
modifications. It is fully compliant with RFC 2516, the official PPPoE
specification.

%description -l pl.UTF-8
PPPoE (Protokół Punkt-Punkt poprzez Ethernet) jest protokołem używanym
przez wielu dostarczycieli usługi ADSL.

Klient jest programem działającym w przestrzeni użytkownika, a to
oznacza, że nie wymaga modyfikacji kernela. Jest w pełni zgodny z
oficjalną specyfikacją PPPoE - RFC 2516.

%description -l pt_BR.UTF-8
PPPoE (Point-to-Point Protocol over Ethernet) é um protocolo usado por
muitos provedores de acesso à internet e companhias telefÔnicas para
prover acesso de alta velocidade xDSL.

Este cliente é um programa user-mode que não necessita de modificações
no kernel. Esta implementação segue a RFC 2516, a especificação
oficial para PPPoE.

%description -l ru.UTF-8
PPPoE (Point-to-Point Protocol over Ethernet) - это протокол,
используемый многими ADSL ISP. Roaring Penguin предоставляет
свободнораспространяемого клиента для подключения к таким ISP.

Клиент представляет собой полностью пользовательскую программу и не
требует каких-либо модификаций ядра. Он полностью совместим с RFC
2516, официальной спецификацией PPPoE.

%description -l uk.UTF-8
PPPoE (Point-to-Point Protocol over Ethernet) - це протокол, який
використовується багатьма ADSL ISP. Roaring Penguin надає вільного
клієнта для підключення до таких ISP.

Клієнт являє собою повністю користувацьку програму і не вимагає
будь-яких модифікацій ядра. Він повністю сумісний з RFC 2516,
офіціальною специфікацією PPPoE.

%package gui
Summary:	GUI front-end for rp-pppoe
Summary(pl.UTF-8):	Graficzny interfejs dla rp-pppoe
Summary(pt_BR.UTF-8):	Interface gráfica para configuração do rp-pppoe
Group:		X11/Applications/Networking
Requires:	rp-pppoe >= 3.4

%description gui
This package contains the graphical frontend (Tk-based) for rp-pppoe.

%description gui -l pl.UTF-8
Graficzny interfejs użytkownika (oparty na Tk) dla rp-pppoe.

%description gui -l pt_BR.UTF-8
Este pacote fornece uma interface gráfica para a configuração do
rp-pppoe.

%package server
Summary:	PPPoE server
Summary(pl.UTF-8):	Serwer PPPoE
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	ppp >= 2.4.1
Requires:	rc-scripts

%description server
PPP over Ethernet server.

%description server -l pl.UTF-8
Serwer PPP over Ethernet.

%package relay
Summary:	PPPoE relay
Summary(pl.UTF-8):	Agent przekazujący pakiety PPPoE
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description relay
PPP over Ethernet relay.

%description relay -l pl.UTF-8
Agent przekazujący pakiety PPPoE.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd src
%{__aclocal}
%{__autoconf}
%configure
# we always want kernel mode PPPoE support in utilities
echo '#define HAVE_LINUX_KERNEL_PPPOE 1' >> config.h
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d}

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C gui install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pppoe-server
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pppoe-server
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/pppoe-relay
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/pppoe-relay

# This is necessary for the gui to work, but it shouldn't be done here !
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ppp/rp-pppoe-gui

# clean docdir
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add pppoe-server
%service pppoe-server restart "PPPoE daemon"

%preun server
if [ "$1" = "0" ]; then
	%service pppoe-server stop
	/sbin/chkconfig --del pppoe-server
fi

%post relay
/sbin/chkconfig --add pppoe-relay
%service pppoe-relay restart "PPPoE relay daemon"

%preun relay
if [ "$1" = "0" ]; then
	%service pppoe-relay stop
	/sbin/chkconfig --del pppoe-relay
fi

%files
%defattr(644,root,root,755)
%doc README doc/*
%attr(755,root,root) %{_sbindir}/pppoe
%attr(755,root,root) %{_sbindir}/pppoe-connect
%attr(755,root,root) %{_sbindir}/pppoe-setup
%attr(755,root,root) %{_sbindir}/pppoe-sniff
%attr(755,root,root) %{_sbindir}/pppoe-st*

%config(noreplace) %{_sysconfdir}/ppp/pppoe.conf
%config(noreplace) %{_sysconfdir}/ppp/firewall-masq
%config(noreplace) %{_sysconfdir}/ppp/firewall-standalone
%{_mandir}/man5/pppoe.conf.*
%{_mandir}/man8/pppoe-connect*
%{_mandir}/man8/pppoe-setup*
%{_mandir}/man8/pppoe-sniff*
%{_mandir}/man8/pppoe-st*
%{_mandir}/man8/pppoe.*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tkpppoe
%attr(755,root,root) %{_sbindir}/pppoe-wrapper
%dir %{_sysconfdir}/ppp/rp-pppoe-gui
%{_datadir}/tkpppoe
%{_mandir}/man1/*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pppoe-server
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%{_mandir}/man8/pppoe-server*
%attr(754,root,root) /etc/rc.d/init.d/pppoe-server
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pppoe-server

%files relay
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pppoe-relay
%{_mandir}/man8/pppoe-relay*
%attr(754,root,root) /etc/rc.d/init.d/pppoe-relay
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pppoe-relay
