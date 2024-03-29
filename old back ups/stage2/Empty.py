from Piece import Piece


class Empty(Piece):
    '''
    Empty object parameters should always be None.
    '''
    def __init__(self, color=None, name=None, img_id=None):
        super().__init__(color, name, img_id)
    
    def __str__(self):
        return "empty"