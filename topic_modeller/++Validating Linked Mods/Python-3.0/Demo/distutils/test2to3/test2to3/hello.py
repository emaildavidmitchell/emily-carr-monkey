def hello():
    try:
        print("Hello, world")
    except IOError as e:
        print(e.errno)
