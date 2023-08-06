import os
import sys
sys.path.append(os.getcwd())

from codev_dashboard import app

app.debug = True
app.run(host='0.0.0.0')
