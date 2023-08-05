from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

#try:  
#    import pypandoc
#    read_md = lambda f: pypandoc.convert(f, 'rst')
#except ImportError:  
#    print("warning: pypandoc module not found, could not convert Markdown to RST")
#    read_md = lambda f: open(f, 'r').read()

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lambda-controller',

    version='0.0.1',

    description='lambda-controller project',
    #long_description=long_description,
    #long_description=read_md('README.md'),

    #url='https://github.com/cloudfish7/lambda-project-creator',

    author='cloudfish7',
    author_email='tskwdev@gmail.com',

    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='aws lambda lambda-controller',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=open('requirements.txt').read().splitlines(),

    #package_data={
    #    'lambda_project_creator': ['template.json','template.txt'],
    #},

    entry_points={
        'console_scripts': [
            'lambda-controller=lambda_controller.shell:main',
        ],
    },
)
