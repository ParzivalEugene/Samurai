class Piece(object):
    def __init__(self, color):
        self.color = color
        self.white = 1
        self.black = 2

    def get_color(self):
        return self.color

    @staticmethod
    def correct_coordinates(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def opponent(self, color):
        return self.black if color == self.white else self.white


class Knight(Piece):
    @staticmethod
    def char():
        return "N"

    def can_move(self, board, x1, y1, x2, y2):
        piece = board.get_piece(x2, y2)
        if piece.get_color() == self.color:
            return False
        return abs((x1 - x2) * (y1 - y2)) == 2 and x1 != x2 and y1 != y2 and self.correct_coordinates(x2, y2)


class King(Piece):
    def __init__(self, color):
        self.was_moved = False
        super().__init__(color)

    @staticmethod
    def char():
        return "K"

    def can_move(self, board, x1, y1, x2, y2):
        piece = board.get_piece(x2, y2)
        if piece.get_color() == self.color:
            return False
        if ((abs(x1 - x2) == abs(y1 - y2) == 1)
            or (abs(x1 - x2) * abs(y1 - y2) == 0
                and (abs(x1 - x2) == 1 or abs(y1 - y2) == 1))) and self.correct_coordinates(x2, y2):
            self.was_moved = True
            return True
        return False


class Queen(Piece):
    @staticmethod
    def char():
        return "Q"

    def can_move(self, board, x1, y1, x2, y2):
        if not self.correct_coordinates(x2, y2):
            return False
        piece = board.get_piece(x2, y2)
        if piece.get_color() == self.color:
            return False
        if x1 == x2 or y1 == y2:
            step = 1 if x2 >= x1 else -1
            for i in range(x1 + step, x2, step):
                if not (board.get_piece(i, y1) is None):
                    return False
            step = 1 if y2 >= y1 else -1
            for j in range(y1 + step, y2, step):
                if not (board.get_piece(x1, j) is None):
                    return False
            return True
        if x1 - y1 == x2 - y2:
            step = 1 if x2 >= x1 else -1
            for i in range(x1 + step, x2, step):
                j = y1 - x1 + i
                if not (board.get_piece(i, j) is None):
                    return False
            return True
        if x1 + y1 == x2 + y2:
            step = 1 if y2 >= y1 else -1
            for j in range(y1 + step, y2, step):
                i = x1 + y1 - j
                if not (board.get_piece(j, i) is None):
                    return False
            return True

    def can_attack(self, board, x1, y1, x2, y2):
        return self.can_move(board, x1, y1, x2, y2)


class Pawn(Piece):
    @staticmethod
    def char():
        return "P"

    def can_move(self, board, x1, y1, x2, y2):
        if x1 != x2 or not self.correct_coordinates(x2, y2):
            return False
        direction, start_row = (1, 1) if self.color == self.white else (-1, 6)
        if x1 + direction == x2:
            return True
        if x1 == start_row and x1 + 2 * direction == x2 and board.field[x1 + direction][y1] is None:
            return True
        return False

    def can_attack(self, board, x1, y1, x2, y2):
        direction = 1 if self.color == self.white else -1
        return x1 + direction == x2 and (y1 + 1 == y2 or y1 - 1 == y2)


class Rook(Piece):
    def __init__(self, color):
        self.was_moved = False
        super().__init__(color)

    @staticmethod
    def char():
        return "R"

    def can_move(self, board, x1, y1, x2, y2):
        if x1 != x2 and y1 != y2 or not self.correct_coordinates(x2, y2):
            return False
        step = 1 if x1 > x2 else -1
        for i in range(x1 + step, x2, step):
            if not (board.get_piece(i, y1) is None):
                return False
        step = 1 if y2 >= y1 else -1
        for j in range(y1 + step, y2, step):
            if not (board.get_piece(x1, j) is None):
                return False
        self.was_moved = True
        return True

    def can_attack(self, board, x1, y1, x2, y2):
        return self.can_move(board, x1, y1, x2, y2)


class Bishop(Piece):
    @staticmethod
    def char():
        return "B"

    def can_move(self, board, x1, y1, x2, y2):
        if not self.correct_coordinates(x2, y2):
            return False
        piece = board.get_piece(x2, y2)
        if not (piece is None) and piece.get_color() == self.color:
            return False
        if x1 - y1 == x2 - y2:
            step = 1 if x2 >= x1 else -1
            for i in range(x1 + step, x2, 0):
                pass