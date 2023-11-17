import types


class Debugger(object):
    attribute_accesses = []
    method_calls = []


class Debuggable:
    def __setattr__(self, item, value):
        Debugger.attribute_accesses.append({
            'action': 'set',
            'class': self,
            'attribute': item,
            'value': value
        })

        return super().__setattr__(item, value)

    def __getattribute__(self, item):
        val = super().__getattribute__(item)
        Debugger.attribute_accesses.append({
            'action': 'get',
            'class': self,
            'attribute': item,
            'value': val
        })

        if type(val) == types.MethodType:
            def log_call(method_class, method_name):
                def log_args(*args, **kwargs):
                    Debugger.method_calls.append({
                        'method': method_name,
                        'class': method_class,
                        'args': (self,) + args,
                        'kwargs': kwargs
                    })

                return log_args

            def call_method_with_log(log_args, method):
                def call_method(*args, **kwargs):
                    log_args(*args, **kwargs)
                    return method(*args, **kwargs)

                return call_method

            return call_method_with_log(log_call(type(self), item), val)
        else:
            return val


class Meta(type):
    def __init__(cls):

        print("__init__2", cls)

    def __new__(cls, *args, **kwargs):
        def init_with_log(x, c):
            def call_init_with_log(c, *args, **kwargs):
                Debugger.method_calls.append(
                    {
                        'method': '__init__',
                        'class': c,
                        'args': (c,) + args,
                        'kwargs': kwargs
                    }
                )
                return x(c, *args, **kwargs)
            return call_init_with_log

        c = type(args[0], (Debuggable,) + args[1], args[2])
        c.__init__ = init_with_log(c.__init__, c)
        return c


class Foo(object, metaclass=Meta):
    def __init__(self, x):
        self.x = x

    def bar(self, v):
        return self.x, v


a = Foo(1)
a.bar(2)

# d = Debuggable()
#
# print(d.y)

print(Debugger.method_calls)
print(Debugger.attribute_accesses)
