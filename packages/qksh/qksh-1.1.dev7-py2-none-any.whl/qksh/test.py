import toggle_sub_daemon as toggle
import re

a = toggle.__file__
print type(a)
print a
b = re.sub('toggle_sub_daemon\.py.*', 'sub_daemon.py', a)
print b