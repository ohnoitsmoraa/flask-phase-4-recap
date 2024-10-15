from app import app
from models import *

with app.app_context():
    # Deleting previous data
    db.session.query(User).delete()
    db.session.query(Post).delete()
    db.session.query(Group).delete()
    db.session.commit()
    # OR
    # User.query.delete()
    # Post.query.delete()
    # Group.query.delete()
    # db.session.delete(user_groups)

    print("Seeding user data............")

    # Adding users
    u1 = User(username="Maureen", email="maureen@gmail.com")
    u2 = User(username="Russell", email="russell@gmail.com")
    u3 = User(username="Mishael", email="mishael@gmail.com")
    u4 = User(username="Pessah", email="pessah@gmail.com")
    u5 = User(username="Brian", email="brian@gmail.com")
    u6 = User(username="Ramah", email="ramah@gmail.com")
    u7 = User(username="Sam", email="sam@gmail.com")
    u8 = User(username="Jennie", email="jennie@gmail.com")
    u9 = User(username="Abby", email="abby@gmail.com")
    u10 = User(username="Jennifer", email="jennifer@gmail.com")

    db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10])
    db.session.commit()

    # Adding posts
    p1 = Post(title="First Post", description="This is my first post", user=u1)
    p2 = Post(title="Second Post", description="This is my second post", user=u2)
    p3 = Post(title="Third Post", description="This is my third post", user=u4)
    p4 = Post(title="Fourth Post", description="This is my fourth post", user=u6)
    p5 = Post(title="Fifth Post", description="This is my fifth post", user=u1)
    p6 = Post(title="Sixth Post", description="This is my sixth post", user=u3)
    p7 = Post(title="Seventh Post", description="This is my seventh post", user=u4)
    p8 = Post(title="Eighth Post", description="This is my eighth post", user=u10)
    p9 = Post(title="Ninth Post", description="This is my ninth post", user=u5)
    p10 = Post(title="Tenth Post", description="This is my tenth post", user=u3)

    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
    db.session.commit()

    print(".............................")

    # Adding groups
    g1 = Group(name="Okwonkwo")
    g2 = Group(name="Marvellous")
    g3 = Group(name="Fabulous")
    g4 = Group(name="Sexy")
    g5 = Group(name="Femmi")

    db.session.add_all([g1, g2, g3, g4, g5])
    db.session.commit()
    
    # Adding users to group
    g1.users.append(u1)
    g3.users.append(u2)
    g2.users.append(u3)
    g5.users.append(u4)
    g4.users.append(u5)
    g1.users.append(u6)
    g3.users.append(u7)
    g5.users.append(u8)
    g2.users.append(u9)
    g4.users.append(u10)

    # Add groups to users
    u1.groups.append(g5)
    u1.groups.append(g3)

    print("Done seeding!")
