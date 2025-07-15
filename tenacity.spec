%global	_disable_lto 1
%global	_disable_ld_no_undefined 1
%global	_cmake_skip_rpath %{nil}
%global	optflags %{optflags} -fPIC

Summary:	An easy-to-use multi-track audio editor and recorder
Name:	tenacity
Version:	1.3.4
Release:	1
License:	GPLv2+
Group:	Sound
Url:	https://codeberg.org/tenacityteam/tenacity
# Submodules are a pain...
#Source0:	https://codeberg.org/tenacityteam/tenacity/archive/%%{name}-v%%{version}.tar.gz
Source0:	%{name}-%{version}.tar.xz
# Porttime is provided by portmidi >= 2.0.4, but the build searches for a separate package
Patch0:	tenacity-1.3.4-workaround-porttimer-library-not-found.patch
Patch1:	tenacity-1.3.4-fix-rpath.patch
Patch2:	tenacity-1.3.4-fix-missing-include.patch
BuildRequires:	cmake > 3.16
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	git
BuildRequires:	python >= 3.7
BuildRequires:	wxwidgets >= 3.1.5
BuildRequires:	yasm
BuildRequires:	gettext-devel
BuildRequires:	ladspa-devel
# Cmake explicitly searches for this
BuildRequires:	jpeg-static-devel
BuildRequires:	%{_lib}wxu3.2-devel
BuildRequires:	wxgtk3.2-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(expat) >= 2.2.9
BuildRequires:	pkgconfig(flac) >= 1.3.3
BuildRequires:	pkgconfig(flac++)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(jsoncpp)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(lame)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libmatroska)
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(lilv-0) >= 0.24.6
BuildRequires:	pkgconfig(lv2) >= 1.16.0
BuildRequires:	pkgconfig(mad)
# Not provided yet - vendored in the sources
#BuildRequires:	pkgconfig(nyquist)
BuildRequires:	pkgconfig(ogg) >= 1.3.4
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(portmidi)
BuildRequires:	pkgconfig(portSMF)
# Included in portmidi >= 2.0.4
#BuildRequires:	pkgconfig(porttime)
BuildRequires:	pkgconfig(RapidJSON)
BuildRequires:	pkgconfig(sbsms) >= 2.1.0
BuildRequires:	pkgconfig(serd-0) >= 0.30.2
BuildRequires:	pkgconfig(sndfile) >= 1.0.28
BuildRequires:	pkgconfig(sord-0) >= 0.16.4
BuildRequires:	pkgconfig(soxr) >= 0.1.3
BuildRequires:	pkgconfig(soundtouch) >= 2.1.2
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(sratom-0) >= 0.6.4
BuildRequires:	pkgconfig(suil-0) >= 0.10.6
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(twolame) >= 0.4.0
BuildRequires:	pkgconfig(vamp-sdk) >= 2.9.0
BuildRequires:	pkgconfig(vorbis) >= 1.3.6
BuildRequires:	pkgconfig(zlib)

%description
This is an easy-to-use multi-track audio editor and recorder. It is not merely
an Audacity fork that removes error reporting and update checking,
although it might seem like it. We have been hard at work implementing our
own features and fixes and want to take Tenacity in a direction our users and
community like.
Features:
* Recording from audio devices (real or virtual).
* Export / Import a wide range of audio formats (extensible with FFmpeg).
* High quality including up to 32-bit float audio support.
* Plug-ins providing support for VST, LV2, and AU plugins.
* Scripting in the built-in scripting language Nyquist, or in Python, Perl and
	other languages with named pipes.
* Editing arbitrary sampling and multi-track timeline.
* Accessibility (editing via keyboard, screen reader and narration support).
* Tools useful in the analysis of signals, including audio.

%files -f %{name}.lang
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/EQDefaultCurves.xml
%{_datadir}/%{name}/nyquist-support/rawwaves/*raw
%{_datadir}/%{name}/nyquist-support/*.lsp
%{_datadir}/%{name}/nyquist-support/*.txt
%{_datadir}/%{name}/plug-ins/*.ny
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*x*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/%{name}.metainfo.xml
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/*.xpm
%{_mandir}/man1/%{name}.1*

#-----------------------------------------------------------------------------

%package libs
Summary:	Libraries needed for %{name}
Group:	System/Libraries

%description libs
An easy-to-use multi-track audio editor and recorder.
This package contains the libraries needed by %{name}.

%files libs
%{_libdir}/%{name}/lib-*.so
%{_libdir}/%{name}/modules/mod-*.so
%{_libdir}/libnyquist.so

#-----------------------------------------------------------------------------

%prep
%autosetup -p1


%build
%cmake -DSBSMS=ON \
		-DTENACITY_BUILD_LEVEL=2

%make_build


%install
%make_install -C build

# Fix desktop file
desktop-file-edit --set-key=Exec --set-value="tenacity %F" \
								%{buildroot}%{_datadir}/applications/%{name}.desktop

# Fix icons placement: NNxNN/%%{name}.png --> NNxNN/apps/%%{name}.png
for N in 16 22 24 32 48;
do
	pushd %{buildroot}%{_iconsdir}/hicolor/${N}x${N}
	mkdir apps
	mv %{name}.png ./apps/
	popd
done

# Drop wrongly installed stuff from sources
rm -f %{buildroot}%{_datadir}/%{name}/help/*

# We take this with our macro
rm -f %{buildroot}%{_datadir}/doc/%{name}/LICENSE.txt

%find_lang %{name}
