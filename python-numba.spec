%global pypi_name numba
%global pypi_version 0.59.0

# Where the src comes from
%global forgeurl https://github.com/numba/numba

# So pre releases can be tried
%bcond_without gitcommit
%if %{with gitcommit}
# a random commit in main 12/2/23
%global commit0 db5f0a45fcccb359cba248c4767cd1caf16c4a85
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%endif

Name:           python-%{pypi_name}
Version:        0.59.0
Release:        1%{?dist}
Summary:        NumPy aware dynamic Python compiler using LLVM

License:        BSD
URL:            https://numba.pydata.org
%if %{with gitcommit}
Source0:        %{forgeurl}/archive/%{commit0}/numba-%{shortcommit0}.tar.gz
Patch0:         0001-numba-setup-lllvmlite.patch
Patch1:         0001-numba-force-version.patch
%else
Source0:        waiting-for-0.59.tar.gz
%endif

BuildRequires:  tbb-devel

BuildRequires:  python3-devel
# Asking for llvmlite 0.42, we have 0.41
BuildRequires:  python3dist(llvmlite) >= 0.41
BuildRequires:  python3dist(numpy) >= 1.11
BuildRequires:  python3dist(numpy) >= 1.22
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(sphinx)

%description
Numba is an open source, NumPy-aware optimizing compiler for Python
sponsored by Anaconda, Inc. It uses the LLVM compiler project to
generate machine code from Python syntax.

Numba can compile a large subset of numerically-focused Python,
including many NumPy functions. Additionally, Numba has support for
automatic parallelization of loops, generation of GPU-accelerated
code, and creation of ufuncs and C callbacks.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

# Asking for llvmlite 0.42, we have 0.41
Requires:       python3dist(llvmlite) >= 0.41
Requires:       python3dist(numpy) >= 1.22

%description -n python3-%{pypi_name}
Numba is an open source, NumPy-aware optimizing compiler for Python
sponsored by Anaconda, Inc. It uses the LLVM compiler project to
generate machine code from Python syntax.

Numba can compile a large subset of numerically-focused Python,
including many NumPy functions. Additionally, Numba has support for
automatic parallelization of loops, generation of GPU-accelerated
code, and creation of ufuncs and C callbacks.

%package -n python3-%{pypi_name}-devel
Summary:        Libraries and headers for %{name}
Requires:       python3-%{pypi_name}%{?_isa} = %{version}-%{release}

%description -n python3-%{pypi_name}-devel
%{summary}

%prep
%if %{with gitcommit}
%autosetup -p1 -n numba-%{commit0}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
%else
# No 0.59 tarball yet
%endif

%build

# For debugging setup.py
export SETUPTOOLS_SCM_DEBUG=1

# numba/np/ufunc/tbbpool.cpp:15:10: fatal error: tbb/version.h: No such file or directory
export NUMBA_DISABLE_TBB=1

%py3_build

%install
%py3_install

# Programatically create the list of dirs
echo "s|%{buildroot}%{python3_sitearch}|%%dir %%{python3_sitearch}|g" > br.sed
find %{buildroot}%{python3_sitearch} -mindepth 1 -type d  > dirs.files
sed -i -f br.sed dirs.files 
cat dirs.files > main.files

# Similar for the python files
find %{buildroot}%{python3_sitearch} -type f -name "*.py" -o -name "*.pyc" -o -name "*.pyi"  > py.files
echo "s|%{buildroot}%{python3_sitearch}|%%{python3_sitearch}|g" > br.sed
sed -i -f br.sed py.files
cat py.files >> main.files

# devel files, headers and such
find %{buildroot}%{python3_sitearch} -type f -name "*.h" -o -name "*.hpp" -o -name "*.cuh" -o -name "*.c" -o -name "*.cu" -o -name "*.gdb" -o -name "*.cpp" -o -name "*.ptx" > devel.files
sed -i -f br.sed devel.files

# Insists on llvmlite 0.42
# %check
# export NUMBA_DISABLE_TBB=1
# %{__python3} setup.py test

%files -n python3-%{pypi_name} -f main.files
%license LICENSE LICENSES.third-party
%doc README.rst
%_bindir/numba

# egg
%{python3_sitearch}/numba*.egg-info/*

# libs
%{python3_sitearch}/numba/*.so
%{python3_sitearch}/numba/core/runtime/*.so
%{python3_sitearch}/numba/core/typeconv/*.so
%{python3_sitearch}/numba/cuda/cudadrv/*.so
%{python3_sitearch}/numba/experimental/jitclass/*.so
%{python3_sitearch}/numba/np/ufunc/*.so

# misc
%{python3_sitearch}/numba/typed/py.typed
%{python3_sitearch}/numba/core/annotations/template.html

#
# devel package
#
%files -n python3-%{pypi_name}-devel -f devel.files

%changelog
* Sat Dec 02 2023 Tom Rix <trix@redhat.com> - 0.59.0-1
- Initial package.
