from web_server import create_app
import sys

app = None
reloader = False
if len(sys.argv) <= 1:
    print('Usage: to run dev, pass some args to this script, else it will run in production mode')
    print('Running on Development config')
    app = create_app(development=True)
    reloader = True
else:
    app = create_app(development=False)
    print('Running on Production config')
    reloader = False

if __name__ == '__main__':
    app.run(use_reloader=False)

