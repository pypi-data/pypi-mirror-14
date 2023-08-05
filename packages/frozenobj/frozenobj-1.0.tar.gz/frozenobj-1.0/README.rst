
Frozen
---------------------------------

Frozen creates an immutable reference to an object. This works (lazily) recursive: mutable members are also frozen upon access. It keeps the original object mutable, returning a proxy class that behaves just like the object except being uneditable. If the underlying object changes, the proxy will reflect this automatically. As such it is immutable in the sense that the reference can't be used to change it, not in the sense that it cannot be changed at all (you could of course discard the original mutable reference). Frozen objects can not be used as dictionary keys.

Installation
---------------------------------

1. `pip install frozenobj`
2. profit

Usage
---------------------------------

Usage is very simple::

	from frozenobj import frozen
	immutable_obj = frozen(mutable_obj)


As a simple example::

	class Cls:
		def __init__(self):
			self.li = [37, 42]
	original = Cls()
	freezered = frozen(original)
	original.li.append(99)   # works
	freezered.li.append(99)  # ImmutableError

Have a look at `tests.py`_ for more examples.

Notes
---------------------------------

* Someone really determined to change your proxy object can find ways to do so. This is not a security measure, it's just a way to enforce your interface (in the purely imaginary case that people don't read or follow the manual saying they shouldn't change things).
* It should work for most objects. It works for classes, class instances, modules, lists, sets, dictionaries and some types derived from them. It implicitly works for ints, floats, strings and tuples which are always immutable (they are returned, not proxied). Functions and methods are also considered constants.
* The `frozen` method is idempotent and uses caching: if you call it twice on the same object, either successively or in parallel, you get the same proxy.
* The recursive freezing on access, while not completely free, should have fairly low computational cost (you need store only values that are accessed a great many times).
* Heavily relies on the `lazy-object-proxy`_ package, which is nice.

License
---------------------------------

Frozen is available under the revised BSD license, see LICENSE.txt. You can do anything as long as you include the license, don't use my name for promotion and are aware that there is no warranty.


.. _tests.py: https://github.com/mverleg/python_frozen/blob/master/tests.py
.. _lazy-object-proxy: https://pypi.python.org/pypi/lazy-object-proxy


