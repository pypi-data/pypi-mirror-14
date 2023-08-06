from setuptools import setup

from txjsonrpc.util import dist


setup(
    name="txJSON-RPC",
    version="0.5",
    description="Code for creating Twisted JSON-RPC servers and clients.",
    maintainer="Paul Hummer",
    maintainer_email="paul@eventuallyanyway.com",
    url="http://github.com/rockstar/txjsonrpc",
    license="BSD, GPL",


    packages=dist.findPackages('txjsonrpc'),
    install_requires=['twisted', 'six'],
    long_description=dist.catReST(
        "docs/PRELUDE.txt",
        "README",
        "docs/DEPENDENCIES.txt",
        "docs/INSTALL.txt",
        "docs/USAGE.txt",
        "TODO",
        "docs/HISTORY.txt",
        stop_on_errors=True,
        out=True),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        ],
    )
