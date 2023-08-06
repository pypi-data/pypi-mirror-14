obj2uni
=======

This packages defines the single function, `obj2uni`, which returns
Unicode strings for sequences of any objects. Each string
has the length equal to the length of the corresponding sequence.
Multiple sequences share the same character mapping.
This function can be useful for other packages which operate on strings faster,
e.g. for computing Levenshtein distance.

```Python
>>> from obj2uni import obj2uni
>>> obj2uni((1, 2, 3, None), ('test', 'ham', 'spam', 3.14159))

(('\x01\x02\x03\x00', '\x07\x05\x06\x04'),
 {'\x00': None,
  '\x01': 1,
  '\x02': 2,
  '\x03': 3,
  '\x04': 3.14159,
  '\x05': 'ham',
  '\x06': 'spam',
  '\x07': 'test'})
```

Released under MIT license. Copyright © 2016 Mail.Ru Group LLC.