import platform
import sys
import locale
import subprocess

def get_common_os():
    system = platform.system()
    if system == 'Darwin':
        system = "Mac OS"
        version, _, _ = platform.mac_ver()
    elif system == 'Windows':
        version, _, sp, _ = platform.win32_ver()
        if sp:
            version += ' with ' + sp
    else:
        version = platform.linux_distribution()
        system = version[0].capitalize() + ' GNU/Linux'
        version = version[1]
    
    is_64bits = sys.maxsize > 2**32
    python_ver = platform.python_version()
    python_exec = sys.executable
    python = subprocess.check_output([python_exec, '-V'])
    print python.strip(),
    print system, version, python_exec,
    
    local = locale.getdefaultlocale()
    print ' '.join(local)

get_common_os()

