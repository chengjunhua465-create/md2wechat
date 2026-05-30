from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="md2wechat",
    version="1.0.0",
    author="ChengJunhua",
    description="Convert Markdown to WeChat Official Account article HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chengjunhua465-create/md2wechat",
    py_modules=["md2wechat"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "md2wechat=md2wechat:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markdown",
    ],
)
