from aprp.aprp import make_app, start_proxy

def main():

    app = make_app()
    start_proxy(app)

if __name__ == '__main__':
    main()
