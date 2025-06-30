CREATE TABLE users (
    id UUID NOT NULL PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    password CHAR(60) NOT NULL,
    name VARCHAR(50) NOT NULL,
    bio VARCHAR(150) NOT NULL DEFAULT '',
    role VARCHAR(10) NOT NULL,
    profile_picture VARCHAR(255) NOT NULL,
    followers INTEGER NOT NULL DEFAULT 0 CHECK (followers >= 0),
    followings INTEGER NOT NULL DEFAULT 0 CHECK (followings >= 0),
    points INTEGER NOT NULL DEFAULT 0 CHECK (points >= 0),
    joined_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE follow (
    id_follower UUID NOT NULL,
    id_following UUID NOT NULL,
    followed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id_follower, id_following),
    FOREIGN KEY (id_follower) REFERENCES users(id),
    FOREIGN KEY (id_following) REFERENCES users(id)
);
