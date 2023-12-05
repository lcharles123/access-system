from web_server import create_app


app = create_app(config_type=app_config.Production)

if __name__ == '__main__':
    app.run(use_reloader=True)

