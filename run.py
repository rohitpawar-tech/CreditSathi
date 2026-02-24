import os
import traceback
from app import create_app

env = os.environ.get('FLASK_ENV', 'dev')

try:
    app = create_app(env)
    if __name__ == '__main__':
        print("🚀 Attempting to start Flask Server...")
        app.run(host='0.0.0.0', port=5000, debug=True)

except Exception as e:
    print("\n❌ SERVER CRASHED! Yahan error hai:")
    print(traceback.format_exc())