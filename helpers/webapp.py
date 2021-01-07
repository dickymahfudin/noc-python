import sys
from paramiko import SSHClient
from scp import SCPClient
from variable import SSH_USER, SSH_PASS, DIR_HOME


def progress(filename, size, sent):
    sys.stdout.write("%s's progress: %.2f%%   \r" %
                     (filename, float(sent)/float(size)*100))


def pushToSite(site, file, to):
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(site["ip"], username=SSH_USER, password=SSH_PASS)
        print(f"---- {site['nojs']} {site['site']} ----")
        scp = SCPClient(ssh.get_transport(), progress=progress)
        scp.put(file, recursive=True, remote_path=to)
        print("\ncopy file to root")
        ssh.exec_command(
            f'sudo cp -r {DIR_HOME}/joulestore-web-app/* /var/lib/sundaya/joulestore-web-app/')
        print("Reload Daemon....")
        ssh.exec_command('sudo systemctl daemon-reload')
        print("Restart webapp service....")
        ssh.exec_command('sudo systemctl restart webapp')
        scp.close()
        ssh.close()
        print(f"---- Update Done ----")

    except:
        print(f"---- {site['nojs']} {site['site']} ----")
        print(f"---- Update Failed ----")
