import glob
import re

for path in glob.glob('motioncharts/*'):
    with open(path, 'r') as f:
        file = f.read()
    with open(path, 'w') as newf:
        new_file = re.sub("http://socr.ucla.edu/htmls/HTML5", "/static", file)
        newf.write(new_file)