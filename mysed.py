import re

with open('m003_upwork_v2.html','r') as f:
  contents = f.readlines()

new_contents = []

for line in contents:
  x = re.search('id="(.*)"', line)
  if x and line.endswith('>\n'):
    print(line)
    text_inside = x.group(1) # https://stackoverflow.com/questions/9889635/regular-expression-to-return-all-characters-between-two-special-characters
    new_line = re.sub(f'id="{text_inside}"', f'id="{text_inside}" name="{text_inside}"', line)
    new_contents.append(new_line)
  else:
    new_contents.append(line)

#print(new_contents)
with open('m003_upwork_v3.html','w') as f:
  for line in new_contents:
    f.write(line)
