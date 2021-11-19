users = [
 {"id":0, "name":"Hero"},
 {"id":1, "name":"Dunn"},
 {"id":2, "name":"Sue"},
]

friendship_pairs = [(0,1),(0,2)]

friendships = {user["id"]: [] for user in users}

for i,j in friendship_pairs:
  friendships[i].append(j)
  friendships[j].append(i)

def number_of_friends(user):
  user_id = user["id"]
  friend_ids = friendships[user_id]
  return len(friend_ids)

total_connections = sum(number_of_friends(user) for user in users)
print(total_connections)
