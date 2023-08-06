from functools import reduce

def get_method_and_copy_of_attribute(obj, meth, attr):

    f = return_method(obj, meth)
    x = replace_and_return_attribute(obj, attr)

    return f, x

def return_method(obj, meth):
    return reduce(getattr, meth.split('.'), obj)

def replace_and_return_attribute(obj, attr):

    global x_orig

    attr_path = attr.split('.')

    x_orig = reduce(getattr, attr_path, obj)
    x = x_orig.copy()

    xhead = reduce(getattr, attr_path[:-1], obj)
    xtail = attr_path[-1]

    setattr(xhead, xtail, x)

    return x

def reset_attribute(obj, attr):
    global x_orig
    attr_path = attr.split('.')
    xhead = reduce(getattr, attr_path[:-1], obj)
    xtail = attr_path[-1]
    setattr(xhead, xtail, x_orig)
