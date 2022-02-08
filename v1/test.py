
# def testt(**kwargs):
#     print(kwargs)

#     for k, v in kwargs.items():

#         print(f"{k}, {v}")


# testt(you='testy')


# def hello_world(func):
#     def wrapper():
#         print('top')
#         func()
#         print('bottom')
#     return wrapper


# @hello_world
# def go():
#     print("Hi")


# go()


# def hello_world(func):
#     def wrapper(*args, **kwargs):
#         print(args)
#         print(kwargs)
#         print('top')
#         func(*args, **kwargs)
#         print('bottom')

#     return wrapper


# @hello_world
# def go(name):
#     print("Hi ", name)


# go("jimmy")


# def hello_world(num):
#     def deco(func):
#         def wrapper(*args, **kwargs):
#             print('top')
#             for index in range(num):
#                 result = func(*args, **kwargs)
#             print('bottom')
#             return result
#         return wrapper
#     return deco


# @hello_world(num=8)
# def go(name):
#     print("Hi ", name)


# go("jimmy")


# def hello_world(func):
#     def wrapper(*args, **kwargs):
#         print(args)
#         print(kwargs)
#         print('top')
#         func(*args, **kwargs)
#         print('bottom')

#     return wrapper


# @hello_world
# def go(name):
#     print("Hi ", name)


# go("jimmy")

class testyyy():

    def try_many(num):
        def deco(func):
            def wrapper(*args, **kwargs):
                for i in range(0, num):
                    try:
                        response = func(*args, **kwargs)
                        return response

                    except Exception as ex:
                        print(ex)
                        pass

                return False

            return wrapper
        return deco

    @try_many(num=8)
    def testy_func(self, x, y):
        return x/y


testy = testyyy()
x = 1
y = 0
response = testy.testy_func(x, y)

if response != False:
    print(response)

else:
    print("삐빅 애러입니다.")
