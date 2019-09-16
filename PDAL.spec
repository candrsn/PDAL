Summary:	Point Data Abstraction Library
Name:		PDAL
Version:	2.0.1
Release:	1%{?dist}
License:	BSD
Source:		https://github.com/%{name}/%{name}/archive/%{name}-%{version}-src.tar.gz
URL:		http://www.pdal.io
Source1:	http://download.osgeo.org/proj/vdatum/%{name}-vdatums.zip
#Source1:        http://download.osgeo.org/proj/vdatum/egm08_25/egm08_25.gtx
#Source2:        http://download.osgeo.org/proj/vdatum/egm08_25/egm08_25.txt
#Source3:        http://download.osgeo.org/proj/vdatum/egm96_15/egm96_15.gtx
#Source4:        http://download.osgeo.org/proj/vdatum/egm96_15/WW15MGH.TXT
#Source5:        http://download.osgeo.org/proj/vdatum/vertcon/README.TXT
#Source6:        http://download.osgeo.org/proj/vdatum/vertcon/vertconc.gtx
#Source7:        http://download.osgeo.org/proj/vdatum/vertcon/vertcone.gtx
#Source8:        http://download.osgeo.org/proj/vdatum/vertcon/vertconw.gtx
#Source9:        http://download.osgeo.org/proj/vdatum/usa_geoid1999.zip
#Source10:       http://download.osgeo.org/proj/vdatum/usa_geoid2003.zip
#Source11:       http://download.osgeo.org/proj/vdatum/usa_geoid2009.zip
#Source12:       http://download.osgeo.org/proj/vdatum/usa_geoid2012.zip
#Source13:       http://download.osgeo.org/proj/vdatum/usa_geoid2012b.zip

BuildRequires:	cmake boost-devel >= 1.57, proj >= 4.9.0, boost >= 1.57, glibc-headers
BuildRequires:	postgresql-devel, geos-devel, gdal-devel, libgeotiff-devel
BuildRequires:	pcl-devel, openni-devel, qhull-devel, zlib-devel, eigen3-devel, laszip-devel
BuildRequires:	python3-devel, python3-numpy, jsoncpp-devel, hdf5-devel, netcdf-cxx-devel
Requires:	gdal >= 2.0, libgeotiff >= 1.4.0, pcl >= 1.7.2
Requires:	points2grid >= 1.3.0, laszip >= 3.0.0
Requires:	postgresql, geos, geos-devel, pcl, openni, qhull
Requires:	zlib, eigen3
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description
PDAL is a BSD licensed library for translating and manipulating point cloud
data of various formats. It is a library that is analogous to the GDAL raster
library. PDAL is focussed on reading, writing, and translating point cloud
data from the ever-growing constellation of data formats. While PDAL is not
explicitly limited to working with LiDAR data formats, its wides format
coverage is in that domain.

PDAL is related to Point Cloud Library (PCL) in the sense that both work with
point data, but PDAL’s niche is data translation and processing pipelines, and
PCL’s is more in the algorithmic exploition domain. There is cross over of both
niches, however, and PDAL provides a user the ability to exploit data using
PCL’s techniques.

%package devel
Summary:	PDAL development header files and libraries
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The pdal-devel package contains the header files and libraries needed to
compile C or C++ applications which will directly interact with PDAL.

%package libs
Summary:	The shared libraries required for PDAL
Group:		Development/Libraries

%description libs
The pdal-libs package provides the essential shared libraries for any
PDAL client program or interface. You will need to install this package
to use PDAL

%package vdatums
Summary:        Vertical datum and geoid files for PDAL
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description vdatums
This package contains vertical datum and geoid files for PDAL.

%prep
%setup -q -n %{name}-%{version}-src

%build
%cmake	-D PDAL_LIB_INSTALL_DIR:PATH=%{_lib} \
	-D CMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-D CMAKE_VERBOSE_MAKEFILE=ON  \
	-D CMAKE_BUILD_TYPE=Release \
	-D WITH_GEOTIFF=ON \
	-D GEOTIFF_INCLUDE_DIR=%{_includedir}/libgeotiff \
	-D WITH_LASZIP=ON \
	-D PDAL_HAVE_HEXER=ON \
	-D PDAL_HAVE_GEOS=ON \
	-D PDAL_HAVE_PYTHON=ON \
	-D BUILD_PLUGIN_PYTHON=ON \
	-D BUILD_PLUGIN_HEXBIN=ON \
	-D PDAL_HAVE_LIBGEOTIFF=ON \
	-D BUILD_PLUGIN_PCL=OFF \
	-D PDAL_HAVE_LIBXML2=ON \
	-D BUILD_PLUGIN_PYTHON:BOOL=FALSE \
	-D PDAL_HAVE_NITRO=OFF \
	-D POSTGRESQL_INCLUDE_DIR=%{_includedir}/pgsql \
	-D POSTGRESQL_LIBRARIES=%{_libdir}/libpq.so \
	-D OPENNI2_INCLUDE_DIRS:PATH=%{_includedir}/ni \
	-D OPENNI2_LIBRARY:FILEPATH=%{_libdir}/libOpenNI.so .

make %{?_smp_mflags}

%install
make install/fast DESTDIR=%{buildroot}
# Remove duplicated cmake files
# %{__rm} -f %{buildroot}/usr/lib/pdal/cmake/PDAL*.cmake

# unpack vertical datums
mkdir -p %{buildroot}%{_datadir}/proj
mkdir vdatum
pushd vdatum
unzip -o %{SOURCE1}
mv *.gtx  %{buildroot}%{_datadir}/proj/
popd
rm -rf vdatum

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%license LICENSE.txt
%doc doc/
%{_bindir}/pdal
%{_bindir}/pdal-config

%files libs
%{_libdir}/libpdal_*
%{_libdir}/libpdalcpp.so

%files devel
%{_includedir}/pdal/
%{_libdir}/cmake/PDAL/PDAL*.cmake
#%{_libdir}/pkgconfig/pdal.pc
%{_libdir}/pkgconfig/*.pc

%files vdatums
%attr(0644,root,root) %{_datadir}/proj/*.gtx

%changelog
* Mon Apr 01 2019 Markus Neteler <neteler@mundialis.de> 1.8.0-2
- fix for "nothing provides pkgconfig(geos) needed by PDAL-devel..."

* Wed Nov 07 2018 Markus Neteler <neteler@mundialis.de> 1.8.0-1
- New 1.8.0 upstream release

* Mon May 14 2018 Markus Neteler <neteler@mundialis.de> 1.7.2-2
- New 1.7.2 upstream release
- hexer no longer required

* Thu May 10 2018 Markus Neteler <neteler@mundialis.de> 1.7.2-1
- New 1.7.2RC2 upstream release
- enforce python3
- set -DBUILD_PLUGIN_PYTHON:BOOL=FALSE to avoid numpy detection error

* Fri Apr 20 2018 Markus Neteler <neteler@mundialis.de> 1.7.0-1
- New 1.7.0 upstream release
- patch for https://github.com/PDAL/PDAL/issues/1899
- patch using https://github.com/PDAL/PDAL/pull/1900

* Thu Dec 14 2017 Markus Neteler <neteler@mundialis.de> 1.6.0-3
- fix pkgconfig (must be in -devel)

* Sat Oct 28 2017 Markus Neteler <neteler@mundialis.de> 1.6.0
- New 1.6.0 upstream release

* Tue Oct 24 2017 Markus Neteler <neteler@mundialis.de> 1.5.0
- New 1.5.0 upstream release
- vertical datums added

* Sun Jan  8 2017 Markus Neteler <neteler@osgeo.org> 1.4.0
- New upstream release
- configure tweaks

* Sat Jun 20 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.9-4
- Change build type from Debug to Release

* Mon Apr 20 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.9-3
- Various updates:
 - Build with hexer support
 - Own directories in devel subpackage
 - omit deprecated Group: tags and %%clean section
 - Use better macros for make and cmake
 - use %%{?_isa} macro in subpkg dependencies
 - have %%build section envoke 'make'
 - Update %%install section
 - Improve cmake build parameters
 - Use %%license macro
 - Add %%doc
 - Get rid of BuildRoot definition
 - No need to cleanup buildroot during %%install
 - Remove %%defattr
 - Run ldconfig
 - Add PostgreSQL and PointCloud support
 - Add Python and PCL plugins
 - Build with GEOS and OPENNI2 support
 - Update BR and Requires
 - Add -libs subpackage, and move related files there

* Fri Apr 10 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.9-2
- Add -devel subpackage, and move related files there.

* Fri Apr 10 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.9-1
- Update to 0.9.9

* Tue Mar 10 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.8-3
- Add support for more stuff.

* Sun Mar 8 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.8-2
- Rebuild with new GDAL and the new build points2grid.

* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.8-1
- Initial packaging

