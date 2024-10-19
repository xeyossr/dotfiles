from flask import * 
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-songs', methods=['GET'])
def get_songs():
    with open('musics.json', 'r') as f:
        songs = json.load(f)
    return jsonify(songs)

if __name__ == '__main__':
    app.run(debug=True)