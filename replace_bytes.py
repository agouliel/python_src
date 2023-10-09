# first convert string to bytes, then replace, then back to string
# inspired by https://www.youtube.com/watch?v=sgHbC6udIqc
# Pragmatic Unicode, or, How do I stop the pain? - Ned Batchelder - Mar 16, 2012

a = '\u0386\u03bb\u03b5\u03be' # 'Alex' in greek

# replace str
a.replace('\u03b5', 'e')

# replace bytes
a.encode().replace(b'\xce\xb5', b'e').decode()
