import telnetlib


def clear_line(host, port):
    user = "lab\n"
    password = "lab\n"
    user.encode('utf-8')
    password.encode('utf-8')

    tn = telnetlib.Telnet(host)
    try:
        match = tn.expect([b"Username: ", b"Password: "], timeout=10)
        if (match[0] == 0):
            tn.write(b"lab\n")
        elif (match[0] == 1):
            tn.write(b"lab\n")
            tn.write(b"enable\n")
        else:
            print("Clear line might fail now !")
        if password:
            tn.read_until(b"Password: ", timeout=10)
            tn.write(b"lab\n")

        line_port = int(port) - 2000
        clear_line_cmd = ("clear line %d\n" % line_port).encode('ascii')
        tn.write(clear_line_cmd)
        tn.write(b"\n")

        tn.write(b"exit\n")
        tn.read_all()
    except EOFError as err:
        print("Clear line has failed for {host}:{port} | {err} ".format(
            host=host, port=port, err=str(err)))
