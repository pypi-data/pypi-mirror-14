"""
Build trimxtreme.

Cython is run when
* no pre-generated C sources are found,
* or the pre-generated C sources are out of date,
* or when --cython is given on the command line.
"""
import sys
import os.path
from distutils.core import setup, Extension
from distutils.version import LooseVersion

from trimxtreme import __version__

MIN_CYTHON_VERSION = '0.17'

if sys.version_info < (2, 6):
	sys.stdout.write("At least Python 2.6 is required.\n")
	sys.exit(1)


def out_of_date(extensions):
	"""
	Check whether any pyx source is newer than the corresponding generated
	C source or whether any C source is missing.
	"""
	for extension in extensions:
		for pyx in extension.sources:
			path, ext = os.path.splitext(pyx)
			if ext not in ('.pyx', '.py'):
				continue
			csource = path + ('.cpp' if extension.language == 'c++' else '.c')
			if not os.path.exists(csource) or (
				os.path.getmtime(pyx) > os.path.getmtime(csource)):
				return True
	return False


def no_cythonize(extensions, **_ignore):
	"""
	Change file extensions from .pyx to .c or .cpp.

	Copied from Cython documentation
	"""
	for extension in extensions:
		sources = []
		for sfile in extension.sources:
			path, ext = os.path.splitext(sfile)
			if ext in ('.pyx', '.py'):
				if extension.language == 'c++':
					ext = '.cpp'
				else:
					ext = '.c'
				sfile = path + ext
			sources.append(sfile)
		extension.sources[:] = sources
	return extensions


def cythonize_if_necessary(extensions):
	if '--cython' in sys.argv:
		sys.argv.remove('--cython')
	elif out_of_date(extensions):
		sys.stdout.write('At least one C source file is missing or out of date.\n')
	else:
		return no_cythonize(extensions)

	try:
		from Cython import __version__ as cyversion
	except ImportError:
		sys.stdout.write(
			"ERROR: Cython is not installed. Install at least Cython version " +
			str(MIN_CYTHON_VERSION) + " to continue.\n")
		sys.exit(1)
	if LooseVersion(cyversion) < LooseVersion(MIN_CYTHON_VERSION):
		sys.stdout.write(
			"ERROR: Your Cython is at version '" + str(cyversion) +
			"', but at least version " + str(MIN_CYTHON_VERSION) + " is required.\n")
		sys.exit(1)

	from Cython.Build import cythonize
	return cythonize(extensions)


extensions = [
	Extension('trimxtreme._align', sources=['trimxtreme/_align.pyx']),
	Extension('trimxtreme._qualtrim', sources=['trimxtreme/_qualtrim.pyx']),
	Extension('trimxtreme._seqio', sources=['trimxtreme/_seqio.pyx']),
]
extensions = cythonize_if_necessary(extensions)

setup(
	name = 'trimxtreme',
	version = __version__,
	author = 'Albert Vilella',
	author_email = 'avilella@gmail.com',
	url = 'https://bitbucket.org/avilella/cegx-barcoding',
	description = 'modified version of 8-lettered software to trim adapters from high-throughput sequencing reads',
	license = 'MIT',
	ext_modules = extensions,
	packages = ['trimxtreme', 'trimxtreme.scripts'],
	scripts = ['bin/trimxtreme'],
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Environment :: Console",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Programming Language :: Cython",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Topic :: Scientific/Engineering :: Bio-Informatics"
	]
)
