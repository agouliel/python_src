# https://twitter.com/driscollis/status/1459274780306198538

class decorator_with_arguments:
  def __init__(self, argl, arg2) :
    print("in init" )
    self.argl = argl
    self.arg2 = arg2
    print( 'Decorator args: {}, {}'.format(argl, arg2))

  def __call__(self, f):
    print( "in _call")
    def wrapped(*args, **kwargs):
      print( "in wrapped()")
      return f(*args, **kwargs)
    return wrapped

@decorator_with_arguments(3, 'Python' )
def doubler (number) :
  return number * 2

print (doubler(5))

# output:
# in init
# Decorator args: 3, Python
# in _call
# in wrapped()
# 10
