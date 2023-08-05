from tasks import single as s
import unittest


class SingletonTest(unittest.TestCase):
    """Tests for the singleton task"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_method_1(self):
        """
        test for method1
        :return:
        """
        f = s.Foo.get_instance()
        g = s.Foo.get_instance()
        self.assertTrue(f is g)

    def test_method_2(self):
        """
        test for method2
        :return:
        """

        @s.make_it_singleton
        class Goo:
            def __init__(self, name):
                self.name = name

        a = Goo("gal")
        b = Goo("tomer")

        # extract the type of the wrapped class from the closure. note that the
        # closure contains cells, so we need to also extract the data from the cell

        the_class = Goo.__closure__[0].cell_contents
        self.assertTrue(isinstance(b, the_class))
        self.assertTrue(a is b)

    def test_method_3(self):
        """
        test for method3
        :return:
        """

        @s.MakeItSingleton
        class Goo:
            def __init__(self, name):
                self.name = name

        a = Goo("gal")
        b = Goo("tomer")

        self.assertTrue(isinstance(b, Goo.c))
        self.assertTrue(a is b)

    def test_method_4_again(self):
        """
        test for method4
        :return:
        """
        @s.make_it_singleton_2
        class Goo:
            def __init__(self, name):
                self.name = name

        a = Goo("gal")
        b = Goo("tomer")

        self.assertTrue(isinstance(b, Goo._the_type))
        self.assertTrue(a is b)


if __name__ == '__main__':
    unittest.main()
