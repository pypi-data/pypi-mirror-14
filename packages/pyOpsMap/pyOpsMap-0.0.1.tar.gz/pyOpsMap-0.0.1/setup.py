from setuptools import setup


setup(
    name="pyOpsMap",
    version="0.0.1",

    packages=[
        "pyOpsMap"
    ],

    author="Tyler Agee",
    author_email="tyler@pyroturtle.com",
    url="https://github.com/tekton/pyOpsMap",
    license="MIT",
    description="Mapping operators to a dictionary switch",
    long_description="Check the file README.md",
    keywords="operator",
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={"pyOpsMap": ["README.md"]}
)
