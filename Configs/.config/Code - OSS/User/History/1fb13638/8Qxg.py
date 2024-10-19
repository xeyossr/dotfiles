from flask import Flask, request, jsonify
from stockfish import Stockfish

app = Flask(__name__)

# Stockfish motoru yolunu belirtin
stockfish = Stockfish("/usr/bin/stockfish")

@app.route('/get_best_move', methods=['POST'])
def get_best_move():
    data = request.json
    fen_position = data.get("fen_position")
    player_color = data.get("player_color", "w")

    stockfish.set_fen_position(fen_position)

    if player_color == "b":
        stockfish.set_option("UCI_White", False)  # Siyah oynuyor
    else:
        stockfish.set_option("UCI_White", True)   # Beyaz oynuyor

    best_move = stockfish.get_best_move()
    
    return jsonify({"best_move": best_move})

if __name__ == '__main__':
    app.run(debug=True)
