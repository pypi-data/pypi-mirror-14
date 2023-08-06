"""A setup module for the Datastore v1beta3 protocol definitions."""

import setuptools

install_requires = [
    'protobuf==3.0.0b1.post2'
]


setuptools.setup(
    name='proto-google-datastore-v1beta3',
    version='1.0.0-beta.1',

    author='Google Inc',
    author_email='gcd-discuss@google.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7'
    ],
    description=('Generated files from protocol buffers'
                 ' for Cloud Datastore v1beta3.'),
    install_requires=install_requires,
    license='Apache',
    packages=setuptools.find_packages(),
    url='https://github.com/GoogleCloudPlatform/google-cloud-datastore'
)
