import sys
from portfolio import create_app, db
from portfolio.models import User
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: create_user.py <username> <password>')
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    app = create_app()
    with app.app_context():
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        print(f'User {username} created successfully!')