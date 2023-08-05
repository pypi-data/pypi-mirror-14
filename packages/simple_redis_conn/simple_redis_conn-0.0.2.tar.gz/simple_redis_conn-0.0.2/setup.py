from setuptools import setup


setup(
    name="simple_redis_conn",
    version="0.0.2",
    packages=[
        "simple_redis_conn"
    ],
    author="Tyler Agee",
    author_email="tyler@pyroturtle.com",
    url="https://github.com/tekton/simple_redis_conn_python",
    license="MIT License",
    description="Mapping operators to a dictionary switch",
    long_description="Check the file README.md",
    keywords="operator",
    install_requires=['redis', 'hiredis'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={"simple_redis_conn": ["README.md"]}
)
