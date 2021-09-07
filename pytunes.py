import xmltodict

data = xmltodict.parse(open("Library_songs.xml").read())

tracks = data['plist']['dict']['dict']['dict']

for i in tracks:
  # print name, artist, composer, album

  # if both Album Artist and Composer exist, then Composer is 4th (index 3) and Album is 5th
  if ('Album Artist' in i['key'] and 'Composer' in i['key']):
    print(i['string'][0] + "@" + i['string'][1] + "@" + i['string'][3] + "@" + i['string'][4])

  # only Album Artist, so composer doesn't exist and Album is 4th
  elif 'Album Artist' in i['key']:
    print(i['string'][0] + "@" + i['string'][1] + "@@" + i['string'][3])

  # only Composer, so Album is again 4th
  elif 'Composer' in i['key']:
    print(i['string'][0] + "@" + i['string'][1] + "@" + i['string'][2] + "@" + i['string'][3])

  # neither exists, so Album is 3rd
  else:
    print(i['string'][0] + "@" + i['string'][1] + "@@" + i['string'][2])
