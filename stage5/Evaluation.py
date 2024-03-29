
class Evaluation():
    def __init__(self) -> None:
        pass

    developmentBooleans = {
        "whiteCastle" : False,
        "whiteKnight1": False,
        "whiteKnight2" : False,
        "whiteBishop1" : False,
        "whiteBishop2" : False,
        "blackCastle": False,
        "blackKnight1": False,
        "blackKnight2" : False,
        "blackBishop1" : False,
        "blackBishop2" : False,
    }

    def getEvaluation(gameBoard):
        '''
        Get game evaluation. evaluation > 0 means white is winning, evaluation < 0 means black is winning. 
        A pawn is worth 1 evaluation point. For example, if white is 3 pawns up, then evaluation is approximately 3.
        Returns:
            int evaluation
        '''
        materialBalance = Evaluation.countMaterial(gameBoard)
        pawnProgressionAdvantage = Evaluation.pawnProgression(gameBoard)
        developmentAdvantage = Evaluation.getDevelopmentScore(gameBoard)
        
        evaluation = materialBalance + pawnProgressionAdvantage + developmentAdvantage

        return evaluation

    def countMaterial(gameBoard):
        '''
        Returns: materialBalance
        '''
        # Count material
        whiteMaterial = 0
        blackMaterial = 0
        for row in range(8):
            for col in range(8):
                if gameBoard[row][col].color == "white":
                    whiteMaterial += gameBoard[row][col].value
                elif gameBoard[row][col].color == "black":
                    blackMaterial += gameBoard[row][col].value

        materialBalance = whiteMaterial - blackMaterial
        # print(f"Material balance: {materialBalance}")
        return materialBalance
    
    def pawnProgression(gameBoard):
        '''
        rewards pushing a pawn
        '''
        whitePawnProgression = 0
        blackPawnProgression = 0
        for row in range(8):
            for col in range(8):
                if gameBoard[row][col].color == "white" and gameBoard[row][col].name == "pawn":
                    whitePawnProgression += (7 - row) * 0.1
                if gameBoard[row][col].color == "black" and gameBoard[row][col].name == "pawn":
                    blackPawnProgression += (row) * 0.1
        pawnProgressionAdvantage = round(whitePawnProgression - blackPawnProgression, 2)
        return pawnProgressionAdvantage
    
    def getDevelopmentScore(gameBoard):
        '''
        rewards castling, even if its not safe
        rewards developing bishop or knight
        Returns:
            score (int): 2 for castling, 0.2 for developing bishop or knight
            -1 if no move given
        '''
        score = 0
        # If bishop's or knight's starting square is empty but it has not been emptied on the main board yet
        # White knights
        if gameBoard[7][1].name != "knight" and \
            Evaluation.developmentBooleans["whiteKnight1"] == False:
            score += 0.2
        if gameBoard[7][6].name != "knight" and \
            Evaluation.developmentBooleans["whiteKnight2"] == False:
            score += 0.2
        # Black knights
        if gameBoard[0][1].name != "knight" and \
            Evaluation.developmentBooleans["blackKnight1"] == False:
            score -= 0.2
        if gameBoard[0][6].name != "knight" and \
            Evaluation.developmentBooleans["blackKnight2"] == False:
            score -= 0.2
        # White bishops
        if gameBoard[7][2].name != "bishop" and \
            Evaluation.developmentBooleans["whiteBishop1"] == False:
            score += 0.2
        if gameBoard[7][5].name != "bishop" and \
            Evaluation.developmentBooleans["whiteBishop2"] == False:
            score += 0.2
        # Black bishops
        if gameBoard[0][2].name != "bishop" and \
            Evaluation.developmentBooleans["blackBishop1"] == False:
            score -= 0.2
        if gameBoard[0][5].name != "bishop" and \
            Evaluation.developmentBooleans["blackBishop2"] == False:
            score -= 0.2
        
        # Castling
        if ((gameBoard[7][6].name == "king" and gameBoard[7][5].name == "rook") or \
            (gameBoard[7][2].name == "king" and gameBoard[7][3].name == "rook")) and \
            Evaluation.developmentBooleans["whiteCastle"] == False:
            score += 0.8
        
        if ((gameBoard[0][6].name == "king" and gameBoard[0][5].name == "rook") or \
            (gameBoard[0][2].name == "king" and gameBoard[0][3].name == "rook")) and \
            Evaluation.developmentBooleans["blackCastle"] == False:
            score -= 0.8

        return score
