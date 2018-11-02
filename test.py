from flask import Flask

app = Flask(__name__)


@app.route('/position/')
@app.route('/position/<int:pos>')
def set_position(pos=5):
    return f'got {pos}'

if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        pass