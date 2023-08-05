class Foo:
    _instance = None

    @staticmethod
    def get_instance():
        """
        method_1
        This is the manual implementation of the singleton pattern
        It's a java like implementation
        :return:
        """
        if Foo._instance is None:
            Foo._instance = Foo()
        return Foo._instance


def make_it_singleton(c):
    """
    method2 - function decorator
    :param c: The class to warp, this decorator receives wrap it with the function
     "get_instance" (which adds to it the singleton feature) and then returns the function.
    :return: get_instance, function
    """
    instance = {}

    def get_instance(*args, **kwargs):
        if len(instance) == 0:
            instance[c] = c(*args, **kwargs)
        return instance[c]

    return get_instance


class MakeItSingleton:
    """
        method3 - Class decorator
        This class warps a given class and give it singleton features

        :return: when applied as decorator, an instance of MakeItSingleton
    """

    def __init__(self, c):
        self.c = c
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.c(*args, **kwargs)
            print self.instance
        return self.instance


def make_it_singleton_2(c):
    """
    method4
    :param c:
    :return: class Wrap
    """

    class Wrap(object):
        _the_type = c
        _instance = None

        def __new__(cls, *args, **kwargs):
            if Wrap._instance is None:
                Wrap._instance = c(*args, **kwargs)
            return Wrap._instance

        def __init__(self, *args, **kwargs):
            pass

    return Wrap


def main():
    # A = MakeItSingelton(A)
    # A is an object of type MakeItSingelton
    @MakeItSingleton
    class A:
        def __init__(self, name):
            self.name = name

    print(isinstance(A, MakeItSingleton))
    a = A('Gal')
    b = A('Tomer')

    print(a, a.name)
    print(b, b.name)
    print(a is b)

    print("testing B")

    @make_it_singleton_2
    class B:
        def __init__(self, name):
            self.name = name

    print(B)
    x = B("xx")
    y = B("yy")
    print(x)
    print(y)
    print(x is y)


main()
