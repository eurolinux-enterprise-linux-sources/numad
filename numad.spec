Name: numad
Version: 0.5
Release: 11.20140620git%{?dist}
Summary: NUMA user daemon

License: LGPLv2
Group: System Environment/Daemons
URL: http://git.fedorahosted.org/git/?p=numad.git
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   git clone git://git.fedorahosted.org/numad.git numad-0.5git
#   tar -cJ --exclude-vcs -f numad-0.5git.tar.xz numad-0.5git/
Source0: %{name}-%{version}git.tar.xz
Source1: %{name}.logrotate
Patch0: numad-0.5git-pthread.patch
Patch1: numad-0.5git-version.patch

Requires: initscripts, libcgroup
Requires(post): initscripts
Requires(preun): initscripts
Requires(postun): initscripts

ExcludeArch: s390 s390x %{arm}

%description
Numad, a daemon for NUMA (Non-Uniform Memory Architecture) systems,
that monitors NUMA characteristics and manages placement of processes
and memory to minimize memory latency and thus provide optimum performance.

%prep
%setup -q -n %{name}-%{version}git
%patch0 -p0
%patch1 -p1

%build
make CFLAGS="-std=gnu99 -g" LDFLAGS="-lpthread -lrt -lm"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{_mandir}/man8/
install -p -m 644 numad.conf %{buildroot}%{_sysconfdir}/
install -p -m 755 numad.init %{buildroot}%{_initddir}/numad
install -p -m 644 %SOURCE1 %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
make install prefix=%{buildroot}/usr

%files
%{_bindir}/numad
%{_initddir}/numad
%config(noreplace) %{_sysconfdir}/numad.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/numad
%doc %{_mandir}/man8/numad.8.gz

%post
/sbin/chkconfig --add numad

%preun
if [ $1 -eq 0 ]; then
  # package removal
  /sbin/service numad stop &>/dev/null || :
  /sbin/chkconfig --del numad
fi

%postun
if [ $1 -eq 2 ]; then
  # package upgrade
  /sbin/service numad condrestart &>/dev/null || :
fi

%changelog
* Tue Aug 26 2014 Jan Synáček <jsynacek@redhat.com> - 0.5-11.20140620git
- Release bump
- Related: #1011908

* Mon Jun 23 2014 Jan Synáček <jsynacek@redhat.com> - 0.5-10.20140620git
- Version update
- Resolves: #872524 #999062 #1011908

* Wed Aug 14 2013 Jan Synáček <jsynacek@redhat.com> - 0.5-9.20130814git
- Version update
- Resolves: #987559 #987563
- Add logrotate config
- Resolves: #913546

* Mon Dec 03 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-8.20121015git
- Version update for beta
- Related: #830919

* Mon Oct 22 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-7.20121015git
- Fix srpm rebuild (after update)
- Related: #825153

* Mon Oct 15 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-6.20121015git
- update source (20121015) and makefile patch
- Resolves: #830919

* Wed Sep 12 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-5.20120522git
- fix srpm rebuild
- Resolves: #825153

* Wed May 23 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-4.20120522git
- update source (20120522) and manpage

* Fri Mar 16 2012 Jan Synáček <jsynacek@redhat.com> 0.5-3.20120316git
- update initscript to respect guidelines
- additional minor fixes

* Tue Mar 06 2012 Jan Synáček <jsynacek@redhat.com> 0.5-2.20120221git
- update source
- drop the patch

* Wed Feb 15 2012 Jan Synáček <jsynacek@redhat.com> 0.5-1.20120221git
- spec update

* Fri Feb 10 2012 Bill Burns <bburns@redhat.com> 0.5-1
- initial version
