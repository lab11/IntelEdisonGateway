
import subprocess
import sys
import os
import stat

def main():
    if len(sys.argv) != 3 or (sys.argv[2] != 'start' and sys.argv[2] != 'stop'):
        print('Invalid syntax')
        print('correct syntax: python cellular_network.py device start|stop')
        print('Example: python cellular_network.py /dev/cdc-wdm0 start')
        sys.exit(0)
    myDev = sys.argv[1]
    op = sys.argv[2]

    # check if libqmi is install
    p1 = subprocess.Popen(["ldconfig", "-p"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "libqmi"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    if len(output) == 0:
        print('libqmi is not found')
        sys.exit(0)

    # check if device is attached
    if not stat.S_ISCHR(os.stat(myDev).st_mode):
        print('device not found')
        sys.exit(0)

    # get interface name
    sysoutput = subprocess.check_output(['qmicli', '-d', myDev, '-w'])
    ifname = sysoutput[:-1]

    if op == 'start':
        sysoutput = subprocess.check_output(['qmicli', '-d', myDev, '--nas-get-serving-system'])
        sysoutput = sysoutput.split('\n\t')
        if 'registered' not in sysoutput[1]:
            print('Service network error')
            sys.exit(0)

        # bring the interface up
        if subprocess.call(['ifconfig', ifname, 'up']) != 0:
            print('Cannot bring the network {:} up'.format(ifname))
            sys.exit(0)

        # set mode
        sysoutput = subprocess.check_output(['qmicli', '-d', myDev, '--dms-set-operating-mode=online'])
        if 'successfully' not in sysoutput:
            print('cannot set operating mode')
            sys.exit(0)

        # check if APN configuration file exists
        if not os.path.isfile('/etc/qmi-network.conf'):
            print('Cannot find /etc/qmi-network.conf file')
            sys.exit(0)
        
        print('Starting network...')
        subprocess.call(['qmi-network', myDev, 'start'])

        print('Acquiring IP address...')
        sysout = subprocess.check_output(['udhcpc', '-i', ifname])
    elif op == 'stop':
        print('Stopping network...')
        subprocess.call(['qmi-network', myDev, 'stop'])

        # bring the interface down
        if subprocess.call(['ifconfig', ifname, 'down']) != 0:
            print('Cannot bring the network {:} up'.format(ifname))
            sys.exit(0)



if __name__=="__main__":
    main()

    
