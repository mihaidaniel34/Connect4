class Console:
    def __init__(self, game):
        self.game = game
        self.__board = self.game.board
        self.play()

    def play(self):
        while True:
            verdict = self.game.move(self.game.player1, 1, -1, -1)[1]
            if verdict is not None:
                break
            self.draw_board()
            line, column = self.read_data()
            verdict = self.game.move(self.game.player2, 2, line, column)[1]
            if verdict is not None:
                break
        if verdict == "draw":
            self.show_draw_status()
        elif verdict == "win":
            self.show_player_won()
        elif verdict == "lose":
            self.show_player_lost()

    def read_data(self):
        while True:
            s = input("positions start from 0 \n column to play:")
            s.strip()
            try:
                column = int(s)
            except ValueError:
                print('Input has to be an integer!')
            else:
                if 0 <= column < 7:
                    if self.__board.get_bottom_of_column(column) == -1:
                        s = input("column is full \n"
                                  "column to play:")
                        column = int(s)
                    line = self.__board.get_bottom_of_column(column)
                    return line, column

    def draw_board(self):
        print(self.__board)

    def show_player_won(self):
        print("Congratulations! You have won.")
        self.draw_board()

    def show_player_lost(self):
        print("Unfortunately you have lost.")
        self.draw_board()

    def show_draw_status(self):
        print("Game over! It's a draw.")
        self.draw_board()
