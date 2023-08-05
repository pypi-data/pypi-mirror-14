import os
import setuptools

REPODIR = os.path.dirname(os.path.realpath(__file__))

def _get_version(repodir):
    version = 'UNKNOWN'
    init = open(os.path.join(repodir, 'htmloutput', 'htmloutput.py'))
    for line in init.readlines():
        if '__version__' in line and '=' in line:
            version = line.split('=')[-1].strip()
            version = version.replace('"', '').replace("'", '')
            break
    init.close()
    return version

def _get_longdesc(repodir):
    readme = open(os.path.join(repodir, 'README.rst')).read()
    changelog = open(os.path.join(repodir, 'CHANGES.rst')).read()
    return ''.join([
        readme, '\n\n',
        'CHANGELOG\n',
        '=========\n\n',
        changelog
    ])


version = _get_version(REPODIR)
longdesc = _get_longdesc(REPODIR)
setuptools.setup(
    name="nosehtmloutput-2",
    author='Joel Rivera',
    author_email='rivera@joel.mx',
    url="https://github.com/cyraxjoe/nose-html-output",
    download_url="https://github.com/cyraxjoe/nose-html-output/archive/%s.zip" % version,
    description="Nose plugin to produce test results in html.",
    version=version,
    long_description=longdesc,
    license="Apache License, Version 2.0",
    packages=["htmloutput"],
    install_requires=['nose'],
    classifiers=[
        "Environment :: Console",
        "Topic :: Software Development :: Testing",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'nose.plugins.0.10': [
            'html-output = htmloutput:HtmlOutput'
        ]
    }
)
