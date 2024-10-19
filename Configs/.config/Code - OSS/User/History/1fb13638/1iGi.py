from stockfish import Stockfish

stockfish = Stockfish("/usr/bin/stockfish") 

# Pozisyonu FEN notasyonu ile belirleyelim
def get_best_move(fen_position, player_color):
    stockfish.set_fen_position(fen_position)  # Pozisyonu ayarla
    if player_color == "b":
        stockfish.set_option("UCI_White", False)  # Siyah oynuyor
    else:
        stockfish.set_option("UCI_White", True)  # Beyaz oynuyor
    return stockfish.get_best_move()  # En iyi hamleyi döndür

# Örnek FEN pozisyonu
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
best_move = get_best_move(fen, "w")
print(f"Best move for white: {best_move}")
