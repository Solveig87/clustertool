#! /usr/bin/env python
from frontend import app

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=False, threaded=True)
