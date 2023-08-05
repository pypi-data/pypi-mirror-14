# -*- coding: utf-8 -*-

from functools import wraps
import keystone.api_allow_classes
import inspect

def _get_caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method
    del parentframe
    return name

def keystone_class(original_class):
    keystone.api_allow_classes.__all__.append('.'.join([original_class.__module__, original_class.__name__]))
    for attr_name, attr_value in original_class.__dict__.items() :
        if not attr_name.startswith('__')  and isinstance(attr_value, types.FunctionType):
            setattr(original_class, attr_name, api_callable_check(attr_value))
    return original_class

def api_callable_check(func):
    '''
    api_callable_check decorator
    WARNNING: api_callable_check MUST BE the top decorator
    '''
    @wraps(func)
    def warpped(*args, **kwargs):
        if hasattr(func, 'is_api_method'):
            return func(*args, **kwargs)
        caller = _get_caller_name()
        caller_module = '.'.join(caller[:-1])
        if caller_module in keystone.api_allow_classes.__all__:
            return func(*args, **kwargs)
        else:
            raise NotImplementedError('function "' + func.__name__ + '" not implemented!')

    return warpped

def api_method(func):
    '''
    api method decorator
    '''
    @wraps(func)
    def warpped(*args, **kwargs):
        return func(*args, **kwargs)

    warpped.is_api_method = 1
    return warpped
