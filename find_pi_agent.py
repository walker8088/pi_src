#!/usr/bin/env python
import sys
import time
from socket import *
import netifaces
from daemon import *

PORT = 21578

from daemon import runner
from lockfile import LockTimeout

def is_server_ok(host_ip):
	s = socket(AF_INET, SOCK_STREAM)
	s.settimeout(5)
	try:
		s.connect((host_ip, 80))
		s.close()
		ret = True
	except :
		ret = False
		
	return ret
	
def get_all_ip():
	ip_str = gethostname() + ' '
	iface_names = netifaces.interfaces()
	for iface_name in iface_names:
		if iface_name == 'lo':
			continue
		addrs = netifaces.ifaddresses(iface_name)
		if netifaces.AF_INET in addrs :
			ip_str += iface_name + ':' + addrs[netifaces.AF_INET][0]['addr'] + '  '

	return ip_str
    

class MyApp():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null' #'/dev/tty'
        self.stderr_path = '/dev/null' #'/dev/tty'
        self.pidfile_path =  '/tmp/send_ip.py.pid'
        self.pidfile_timeout = 5
	
    def run(self):
	if is_server_ok('60.216.4.132'):
		pass
		
	#sock = socket(AF_INET, SOCK_DGRAM)
	#sock.bind(('', 0))
	#sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		
	while True:
		try:
		    sock = socket(AF_INET, SOCK_DGRAM)
                    sock.bind(('', 0))
                    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
                    sock.sendto(get_all_ip(),('<broadcast>', PORT))
                    sock.close()
		except Exception as e:
		    print e
		time.sleep(5)


if __name__ == "__main__":
	
	app = MyApp()
	daemon_runner = runner.DaemonRunner(app)
	
	try:
	    daemon_runner.do_action()
	except LockTimeout:
	    print "Error: couldn't aquire lock"
	    print "the daemon must be run already"
	    print "pls stop it first"
	    #you can exit here or try something else

