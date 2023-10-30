"""holder"""


def testa(**kwargs):
    print("in main func")
    print(kwargs)


def testdeco(func, **kwargs):
    print("in the deco")
    func(**kwargs)
    return testdeco


# holder = testdeco

# holder(func=testa, value=5, value_b=2)

# This can be applied insted of the logging decos
# Is there another way of just not having to pass the args al the way down ?


def add(a, b, c, **kwargs):
    return a + b + c


kwargs = dict(a=1, b=2, c=3, d=4)
print(add(**kwargs))
