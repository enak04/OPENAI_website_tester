import os
import sys

# Adds the Backend folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':

    # app.config['ENV'] = 'development'
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
    # app.config['DEBUG'] = True
    
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port)
    # app.run(port=4000, debug=False, use_reloader=False)

