import sys
from portfolio import create_app, db
from portfolio.models import user_model as um
from werkzeug.security import generate_password_hash


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: create_user.py <id> <username> <password>')
        sys.exit(1)

    id = int(sys.argv[1])
    username = sys.argv[2]
    password = sys.argv[3]

    app = create_app()
    with app.app_context():
        user = um.User(id=id, username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print(f'User {username} created successfully')
