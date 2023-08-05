from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = {}
ext_modules = []

if use_cython:
    ext_modules += [
        Extension("jsonfs.jsonfs", ["jsonfs/jsonfs.pyx"]),
    ]
    cmdclass.update({'build_ext': build_ext})
else:
    ext_modules += [
        Extension("jsonfs.jsonfs", ["jsonfs/jsonfs.c"]),
    ]


setup(
    name='jsonfs',
    packages=['jsonfs'],  # this must be the same as the name above
    version='0.0.2',
    author='Leonard Chan',
    author_email='lchan1994@yahoo.com',
    url='https://github.com/PiJoules/jsonfs',  # use the URL to the github repo
    keywords=["json", "filesystem", "jsonfs", "dict"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Cython',
    ],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)

