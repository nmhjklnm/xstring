

# Lazynote 🚀✨

![PyPI](https://img.shields.io/pypi/v/lazynote)
![License](https://img.shields.io/pypi/l/lazynote)
![Python](https://img.shields.io/pypi/pyversions/lazynote)
![Documentation Status](https://nmhjklnm.github.io/lazynote/)

**Lazynote** is an AI-powered tool that can automatically generate documentation comments for classes, modules, and packages. It also supports the translation and customization of existing comments. 💡📝

## Features 🌟

- **Automatic Generation**: Automatically generate documentation comments for classes, modules, and packages by parsing the Python Abstract Syntax Tree (AST), feeding the relevant key code to AI, and using the Google Docstrings template to generate precise comments. 🛠️
- **Smart Translation**: Translate existing comments, supporting multiple languages. The input can be a Python package, module, or class. If it's a package, it will parse the syntax tree layer by layer, perform source code injection, and inject comments into the source code. 🌐
- **Comment Polishing**: Use AI technology to polish comments for improved readability. A small but powerful feature. 📖✨
- **Flexible Customization**: Easily customize all comments across the entire repository. This framework-level functionality has low-level API extensibility. 🔧

## Installation 📦

You can easily install Lazynote using `pip`:

```sh
pip install lazynote
```

## Quick Start 🚀

Here is a simple example demonstrating how to use Lazynote to automatically generate and manage documentation comments.

```python
import pytest
from lazynote.manager import SimpleManager

manager = SimpleManager(pattern='fill')
manager.traverse(lazyllm_package.components, 
                 skip_modules=['lazyllm.components.deploy.relay.server'])
```

## Features Overview 📚

Lazynote provides the following modes to easily customize all comments across the entire repository using AI and source code:

- **TRANSLATE**: Translate existing comments. 🌍
- **POLISH**: Polish and optimize comments. 💅
- **CLEAR**: Clear existing comments. 🗑️
- **FILL**: Fill in missing comments. 📝

## Documentation 📖

For more detailed information and advanced usage, please refer to our [official documentation](https://lazynote.readthedocs.io/en/latest/). ![Documentation Status](https://readthedocs.org/projects/lazynote/badge/?version=latest)

## Contributing 🌟

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for more information. 💖

## License 📄

This project is licensed under the MIT License. For more details, please refer to [LICENSE](LICENSE). 📝

---

