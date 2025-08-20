import uuid
import random
from faker import Faker

fake = Faker()

roles = ['USER']
profile_pictures = [
    'https://example.com/profile1.png',
    'https://example.com/profile2.png',
    'https://example.com/profile3.png',
]

NUM_USERS = 1_000_000
NUM_FOLLOWS = 2_000_000  # total follows (super follower + random)

user_ids = []

# Step 1: Generate users
with open("insert_users.sql", "w", encoding="utf-8") as f_users:
    for _ in range(NUM_USERS):
        user_id = str(uuid.uuid4())
        user_ids.append(user_id)
        email = fake.unique.email()
        password = fake.sha256()[:60]
        name = fake.first_name()
        bio = fake.text(max_nb_chars=150).replace("'", "''")
        role = random.choice(roles)
        profile_picture = random.choice(profile_pictures)
        followers = 0
        followings = 0
        points = random.randint(0, 5000)
        joined_at = fake.date_time_this_decade().isoformat()

        f_users.write(
            f"INSERT INTO users (id, email, password, name, bio, role, profile_picture, "
            f"followers, followings, points, joined_at) VALUES ("
            f"'{user_id}', '{email}', '{password}', '{name}', '{bio}', '{role}', "
            f"'{profile_picture}', {followers}, {followings}, {points}, '{joined_at}');\n"
        )

# Step 2: Generate follows with one super follower
super_follower = random.choice(user_ids)
follow_set = set()

# Super follower follows all other users (N-1)
for user_id in user_ids:
    if user_id != super_follower:
        follow_set.add((super_follower, user_id))

with open("insert_follows.sql", "w", encoding="utf-8") as f_follows:
    # Write super follower follows first
    for follower, following in follow_set:
        followed_at = fake.date_time_this_decade().isoformat()
        f_follows.write(
            f"INSERT INTO follow (id_follower, id_following, followed_at) VALUES ("
            f"'{follower}', '{following}', '{followed_at}');\n"
        )

    # Add random follows until total NUM_FOLLOWS reached
    while len(follow_set) < NUM_FOLLOWS:
        follower = random.choice(user_ids)
        following = random.choice(user_ids)
        if follower != following and (follower, following) not in follow_set:
            follow_set.add((follower, following))
            followed_at = fake.date_time_this_decade().isoformat()
            f_follows.write(
                f"INSERT INTO follow (id_follower, id_following, followed_at) VALUES ("
                f"'{follower}', '{following}', '{followed_at}');\n"
            )
