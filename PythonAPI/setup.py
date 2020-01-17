from distutils.command.build import build
from setuptools import setup, Extension

# To compile and install locally run "python setup.py build_ext --inplace"
# To install library to Python site-packages run "python setup.py build_ext install"


#: Hack to delay numpy import until after setup_requires
#:
#: https://stackoverflow.com/a/54128391
#:
class MyBuild(build):

    def finalize_options(self):
        super().finalize_options()

        # Make NumPy think that it is not in its setup process
        __builtins__.__NUMPY_SETUP__ = False

        import numpy

        extension = next(
            m for m in self.distribution.ext_modules if m == pycocotools_mask
        )
        extension.include_dirs.append(numpy.get_include())


pycocotools_mask = Extension(
    'pycocotools._mask',
    sources=['../common/maskApi.c', 'pycocotools/_mask.pyx'],
    include_dirs=['../common'],
    extra_compile_args=['-Wno-cpp', '-Wno-unused-function', '-std=c99'],
)

setup(
    name='pycocotools',
    packages=['pycocotools'],
    package_dir={'pycocotools': 'pycocotools'},
    # run-time dependencies
    install_requires=[
        'setuptools>=18.0',
        'numpy',
        'matplotlib>=2.1.0',
    ],
    # build-time dependencies
    setup_requires=[
        'cython>=0.27.3',
        'numpy',
    ],
    version='2.0',
    ext_modules=[pycocotools_mask],
    cmdclass={'build': MyBuild},
)
