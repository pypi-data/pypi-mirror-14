from setuptools import setup


setup(
    name="json_logger",
    version="0.0.1",
    packages=[
        "json_logger"
    ],
    author="Tyler Agee",
    author_email="tyler@pyroturtle.com",
    url="https://github.com/tekton/python_json_logger",
    license="MIT License",
    description="Sending json to a logger",
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
    package_data={"json_logger": ["README.md"]}
)
