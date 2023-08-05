
import types
from lazy_object_proxy import Proxy
from weakref import WeakValueDictionary


class ImmutableError(Exception):
	""" Attempted to change an immutable object. """


def is_mutable(obj):
	"""
	Test whether `obj` is in a list of known immutables. May misclassify immutable objects as mutable.

	(Of course someone could do `function.bla = 42`; this just protects against accidental changes, not hackers.)
	"""
	if obj is None:
		return False
	if isinstance(obj, (int, float, bool, str, tuple, types.MethodType, types.FunctionType, ImmutableProxy)):
		return False
	return True


class ImmutableProxy(Proxy):
	"""
	Immutable proxy; any attempted changes raise an exception (underlying object can still be changed by those that have a reference).
	"""
	def __setattr__(self, name, value, __setattr__=object.__setattr__):
		raise ImmutableError('object "{0:}" is frozenobj; attributes cannot be assigned'.format(self))

	def __delattr__(self, name, __delattr__=object.__delattr__):
		raise ImmutableError('object "{0:}" is frozenobj; attributes cannot be deleted'.format(self))

	def __getattr__(self, name):
		obj = super(ImmutableProxy, self).__getattr__(name)
		return frozen(obj)

	def __setitem__(self, key, value):
		raise ImmutableError('object "{0:}" is frozenobj; items cannot be assigned'.format(self))

	def __delitem__(self, key):
		raise ImmutableError('object "{0:}" is frozenobj; items cannot be deleted'.format(self))

	def __getitem__(self, key):
		obj = super(ImmutableProxy, self).__getitem__(key)
		return frozen(obj)

	def __setslice__(self, i, j, value):
		raise ImmutableError('object "{0:}" is frozenobj; slices cannot be assigned'.format(self))

	def __delslice__(self, i, j):
		raise ImmutableError('object "{0:}" is frozenobj; slices cannot be deleted'.format(self))

	def __getslice__(self, i, j):
		obj = super(ImmutableProxy, self).__getslice__(i, j)
		return frozen(obj)

	def __iadd__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __isub__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __imul__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __idiv__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __itruediv__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __ifloordiv__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __imod__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __ipow__(self, other, *args):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __ilshift__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __irshift__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __iand__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __ixor__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))

	def __ior__(self, other):
		raise ImmutableError(('object "{0:}" is frozenobj; it cannot be changed in place; ' +
			'use e.g. `a=a+1` instead of `a+=1`').format(self))


class ListProxy(ImmutableProxy):
	def append(self, p_object):
		raise ImmutableError('list "{0:}" is frozenobj; it cannot be changed'.format(self))

	def clear(self):
		raise ImmutableError('list "{0:}" is frozenobj; it cannot be changed'.format(self))

	def extend(self, iterable):
		raise ImmutableError('list "{0:}" is frozenobj; it cannot be changed'.format(self))

	def insert(self, index, p_object):
		raise ImmutableError('list "{0:}" is frozenobj; it cannot be changed'.format(self))

	def pop(self, index=None):
		raise ImmutableError('list "{0:}" is frozenobj; it cannot be changed'.format(self))

	def remove(self, value):
		raise ImmutableError('list "{0:}" is frozenobj; it cannot be changed'.format(self))

	def reverse(self):
		raise ImmutableError('list "{0:}" is frozenobj; it cannot be changed'.format(self))

	def sort(self, key=None, reverse=False):
		raise ImmutableError('list "{0:}" is frozenobj; it cannot be changed'.format(self))


class DictProxy(ImmutableProxy):
	def clear(self):
		raise ImmutableError('dictionary "{0:}" is frozenobj; it cannot be changed'.format(self))

	def pop(self, k, d=None):
		raise ImmutableError('dictionary "{0:}" is frozenobj; it cannot be changed'.format(self))

	def popitem(self):
		raise ImmutableError('dictionary "{0:}" is frozenobj; it cannot be changed'.format(self))

	def setdefault(self, k, d=None):
		raise ImmutableError('dictionary "{0:}" is frozenobj; it cannot be changed'.format(self))

	def update(self, E=None, **F):
		raise ImmutableError('dictionary "{0:}" is frozenobj; it cannot be changed'.format(self))



class SetProxy(ImmutableProxy):
	def add(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

	def clear(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

	def difference_update(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

	def discard(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

	def intersection_update(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

	def pop(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

	def remove(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

	def symmetric_difference_update(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

	def update(self, *args, **kwargs):
		raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))


_IMMUTABLES_CACHE = WeakValueDictionary()


def frozen(obj):
	if is_mutable(obj):
		if not _IMMUTABLES_CACHE.get(id(obj), None):
			# print('cache miss for',id(obj))
			proxy = ImmutableProxy
			if isinstance(obj, list):
				proxy = ListProxy
			if isinstance(obj, dict):
				proxy = DictProxy
			if isinstance(obj, set):
				proxy = SetProxy
			imobj = proxy(lambda: obj)
			# print('created', imobj, 'for', obj)
			_IMMUTABLES_CACHE[id(obj)] = imobj
		return _IMMUTABLES_CACHE[id(obj)]
	return obj



# class DetachedProxy(Proxy):
# 	"""
# 	Changes are stored on the proxy but don't change the original instance (underlying object can still be changed by those that have a reference).
# 	"""


