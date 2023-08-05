import toggle_sub_daemon
import re


a = toggle_sub_daemon.__file__

b = re.sub('ihealth_api\.py.*', 'sub_daemon.py', a)
print b