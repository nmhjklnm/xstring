## Quick Start 🚀

Here is a simple example demonstrating how to use Lazynote to automatically generate and manage documentation comments.

```python
import pytest
from lazynote.manager import SimpleManager
manager = SimpleManager(pattern='fill')
manager.traverse(lazyllm_package.components, 
                skip_modules=['lazyllm.components.deploy.relay.server'])