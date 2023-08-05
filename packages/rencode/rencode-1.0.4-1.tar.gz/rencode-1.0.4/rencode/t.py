import rencode

for i in range(1000):
    print("Attempt: ", i)
    if i % 2:
     	f = open("/home/aresch/Downloads/rencode-loads-1444800853.32-False", "rb")
    else:
     	f = open("/home/aresch/Downloads/rencode-loads-1444800853.96-False", "rb")
    try:
        rencode.loads(f.read())
    except Exception as e:
        print(e)
