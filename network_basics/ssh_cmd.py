import paramiko

def ssh_cmd(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, usermame=user, pasword=passwd)

    _, stdout, stderr, = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    import getpass
    # user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter Server IP: ') or '192.168.1.203'
    port = input('Enter Server Port: ') or 2222
    cmd = input('Enter Command: ') or 'id'

    ssh_cmd(ip, port, user, password, cmd)