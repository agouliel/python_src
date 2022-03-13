# https://www.facebook.com/manolisvit/posts/10158903109727730

a = 22022022

for i in range(a):
  if i + int(str(i)[::-1]) == a:
    if len(str(i)) == len(str(int(str(i)[::-1]))):
      print(i, int(str(i)[::-1]))