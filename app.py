# portfolio/app.py

from portfolio import create_app

from base64 import b64encode

app = create_app()
app.jinja_env.globals['b64encode'] = b64encode


if __name__ == '__main__':
    app.run(port=8000, debug=True)
