
import subprocess

def findFTDIDevice():
    p1 = subprocess.Popen(["./displayTTY.sh"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", 'FTDI'], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    if len(output):
        output = output.split()
        return [output[0]]
    else:
        return None
