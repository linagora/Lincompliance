#!/usr/bin/env python3
from api import app

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)
