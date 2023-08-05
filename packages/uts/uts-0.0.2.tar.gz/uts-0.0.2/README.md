## Unsupervised Text Segmentation

### Install

    sudo python setup.py install

### Usage

```python
import uts.c99

document = ['this is a good day', 'good day means good weather',\
            'I love computer science', 'computer science is cool']
model = uts.c99.C99(window=2)
boundary = model.segment(document)
# output: [1, 0, 1, 0]
print boundary
```
