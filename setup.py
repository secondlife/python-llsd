import os

from setuptools import find_packages, setup

root_dir = os.path.dirname(__file__)
with open(os.path.join(root_dir, "README.md")) as f:
    long_description = f.read()


setup(
    name="llsd",
    url="https://github.com/secondlife/python-llsd",
    license="MIT",
    author="Linden Research, Inc.",
    author_email="opensource-dev@lists.secondlife.com",
    description="Linden Lab Structured Data (LLSD) serialization library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    setup_requires=["setuptools_scm<6"],
    use_scm_version={
        'local_scheme': 'no-local-version', # disable local-version to allow uploads to test.pypi.org
    },
    extras_require={
        "dev": ["pytest", "pytest-benchmark", "pytest-cov<3"],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development",
    ],
)
