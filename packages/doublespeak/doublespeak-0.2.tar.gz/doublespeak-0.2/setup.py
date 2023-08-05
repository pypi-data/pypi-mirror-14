from setuptools import setup, find_packages

version = '0.2'
long_desc = open("README.rst").read() + "\n" + open('CHANGES.txt').read()

setup(
    name='doublespeak',
    version=version,
    author='Minddistrict',
    url='https://github.com/minddistrict/doublespeak',
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    keywords='Javascript translations Babel',
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Internationalization",
        "Programming Language :: Python :: 2.7"
        ],
    description="Babel/distutils commands to help with managing Javascript "
                "translations.",
    long_description=long_desc,
    include_package_data=True,
    namespace_packages=[],
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Babel'
        ],
    entry_points={
        'distutils.commands': [
            'compile_js_catalog = doublespeak.message:compile_js_catalog',
            'extract_js_messages = doublespeak.message:extract_js_messages',
            'init_js_catalog = doublespeak.message:init_js_catalog',
            'update_js_catalog = doublespeak.message:update_js_catalog',
        ],
        'distutils.setup_keywords': [
            'js_message_extractors = '
            'doublespeak.message:check_js_message_extractors'
        ]},
    )
