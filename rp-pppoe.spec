Summary:	PPP Over Ethernet client
Summary(pl):	Klient PPP Poprzez Ethernet (PPPoE)
Summary(pt_BR):	Protocolo PPPoE (PPP over Ethernet), usado comumente com modens xDSL
Summary(ru):	PPP Over Ethernet (ÐÏÄÄÅÒÖËÁ xDSL)
Summary(uk):	PPP Over Ethernet (Ð¦ÄÔÒÉÍËÁ xDSL)
Name:		rp-pppoe
Version:	3.5
Release:	4
License:	GPL v2+
Group:		Networking
Source0:	http://www.roaringpenguin.com/pppoe/%{name}-%{version}.tar.gz
# Source0-md5:	97972f8f8f6a3ab9b7070333a6a29c4b
Source1:	%{name}-server.init
Source2:	%{name}-server.sysconfig
Source3:	%{name}-relay.init
Source4:	%{name}-relay.sysconfig
Patch0:		%{name}-ac.patch
Patch1:		%{name}-tkpppoe.in.patch
Patch2:		%{name}-enobufs.patch
Patch3:		%{name}-pppd.patch
URL:		http://www.roaringpenguin.com/pppoe/
BuildRequires:	automake
BuildRequires:	autoconf
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
PPPoE (Protokó³ Punkt-Punkt poprzez Ethernet) jest protoko³em u¿ywanym
przez wielu dostarczycieli us³ugi ADSL.

Klient jest programem dzia³aj±cym w przestrzeni u¿ytkownika, a to
oznacza, ¿e nie wymaga modyfikacji kernela. Jest w pe³ni zgodny z
oficjaln± specyfikacj± PPPoE - RFC 2516.

%description -l pt_BR
PPPoE (Point-to-Point Protocol over Ethernet) é um protocolo usado por
muitos provedores de acesso à internet e companhias telefÔnicas para
prover acesso de alta velocidade xDSL.

Este cliente é um programa user-mode que não necessita de modificações
no kernel. Esta implementação segue a RFC 2516, a especificação
oficial para PPPoE.

%description -l ru
PPPoE (Point-to-Point Protocol over Ethernet) - ÜÔÏ ÐÒÏÔÏËÏÌ,
ÉÓÐÏÌØÚÕÅÍÙÊ ÍÎÏÇÉÍÉ ADSL ISP. Roaring Penguin ÐÒÅÄÏÓÔÁ×ÌÑÅÔ
Ó×ÏÂÏÄÎÏÒÁÓÐÒÏÓÔÒÁÎÑÅÍÏÇÏ ËÌÉÅÎÔÁ ÄÌÑ ÐÏÄËÌÀÞÅÎÉÑ Ë ÔÁËÉÍ ISP.

ëÌÉÅÎÔ ÐÒÅÄÓÔÁ×ÌÑÅÔ ÓÏÂÏÊ ÐÏÌÎÏÓÔØÀ ÐÏÌØÚÏ×ÁÔÅÌØÓËÕÀ ÐÒÏÇÒÁÍÍÕ É ÎÅ
ÔÒÅÂÕÅÔ ËÁËÉÈ-ÌÉÂÏ ÍÏÄÉÆÉËÁÃÉÊ ÑÄÒÁ. ïÎ ÐÏÌÎÏÓÔØÀ ÓÏ×ÍÅÓÔÉÍ Ó RFC
2516, ÏÆÉÃÉÁÌØÎÏÊ ÓÐÅÃÉÆÉËÁÃÉÅÊ PPPoE.

%description -l uk
PPPoE (Point-to-Point Protocol over Ethernet) - ÃÅ ÐÒÏÔÏËÏÌ, ÑËÉÊ
×ÉËÏÒÉÓÔÏ×Õ¤ÔØÓÑ ÂÁÇÁÔØÍÁ ADSL ISP. Roaring Penguin ÎÁÄÁ¤ ×¦ÌØÎÏÇÏ
ËÌ¦¤ÎÔÁ ÄÌÑ Ð¦ÄËÌÀÞÅÎÎÑ ÄÏ ÔÁËÉÈ ISP.

ëÌ¦¤ÎÔ Ñ×ÌÑ¤ ÓÏÂÏÀ ÐÏ×Î¦ÓÔÀ ËÏÒÉÓÔÕ×ÁÃØËÕ ÐÒÏÇÒÁÍÕ ¦ ÎÅ ×ÉÍÁÇÁ¤
ÂÕÄØ-ÑËÉÈ ÍÏÄÉÆ¦ËÁÃ¦Ê ÑÄÒÁ. ÷¦Î ÐÏ×Î¦ÓÔÀ ÓÕÍ¦ÓÎÉÊ Ú RFC 2516,
ÏÆ¦Ã¦ÁÌØÎÏÀ ÓÐÅÃÉÆ¦ËÁÃ¦¤À PPPoE.

%package gui
Summary:	GUI front-end for rp-pppoe
Summary(pl):	Graficzny interfejs dla rp-pppoe
Summary(pt_BR):	Interface gráfica para configuração do rp-pppoe
Group:		X11/Applications/Networking
Requires:	rp-pppoe >= 3.4

%description gui
This package contains the graphical frontend (tk-based) for rp-pppoe.

%description gui -l pl
Graficzny interfejs u¿ytkownika (bazuj±cy na tk) dla rp-pppoe.

%description gui -l pt_BR
Este pacote fornece uma interface gráfica para a configuração do
rp-pppoe.

%package server
Summary:	PPPoE server
Summary(pl):	Serwer PPPoE
Group:		Networking/Daemons
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	ppp >= 2.4.1

%description server
PPP over Ethernet server.

%description -l pl server
Serwer PPP over Ethernet.

%package relay
Summary:	PPPoE relay
Summary(pl):	Agent przekazuj±cy pakiety PPPoE
Group:		Networking/Daemons
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig

%description relay
PPP over Ethernet relay.

%description -l pl relay
Agent przekazuj±cy pakiety PPPoE.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
	RPM_INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C gui install \
	RPM_INSTALL_ROOT=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pppoe-server
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pppoe-server
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/pppoe-relay
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/pppoe-relay

# This is necessary for the gui to work, but it shouldn't be done here !
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ppp/rp-pppoe-gui

%clean
rm -fr $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add pppoe-server
if [ -f /var/lock/subsys/pppoe-server ]; then
        /etc/rc.d/init.d/pppoe-server restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/pppoe-server start\" to start PPPoE daemon."
fi

%preun server
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/pppoe-server ]; then
                /etc/rc.d/init.d/pppoe-server stop 1>&2
        fi
        /sbin/chkconfig --del pppoe-server
fi

%post relay
/sbin/chkconfig --add pppoe-relay
if [ -f /var/lock/subsys/pppoe-relay ]; then
        /etc/rc.d/init.d/pppoe-relay restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/pppoe-relay start\" to start PPPoE relay daemon."
fi

%preun relay
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/pppoe-relay ]; then
                /etc/rc.d/init.d/pppoe-relay stop 1>&2
        fi
        /sbin/chkconfig --del pppoe-relay
fi

%files
%defattr(644,root,root,755)
%doc doc/* README
%attr(755,root,root) %{_sbindir}/adsl*
%attr(755,root,root) %{_sbindir}/pppoe
%attr(755,root,root) %{_sbindir}/pppoe-sniff

%config(noreplace) %{_sysconfdir}/ppp/pppoe.conf
%config(noreplace) %{_sysconfdir}/ppp/firewall-masq
%config(noreplace) %{_sysconfdir}/ppp/firewall-standalone
%{_mandir}/man5/*
%{_mandir}/man8/adsl*
%{_mandir}/man8/pppoe.*
%{_mandir}/man8/pppoe-sniff*

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
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/pppoe-server

%files relay
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pppoe-relay
%{_mandir}/man8/pppoe-relay*
%attr(754,root,root) /etc/rc.d/init.d/pppoe-relay
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/pppoe-relay
