from math import inf
from typing import List, Optional, Tuple

Board = List[str]
WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def winner(board: Board) -> Optional[str]:
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    if " " not in board:
        return "draw"
    return None


def render(board: Board) -> None:
    labels = [cell if cell != " " else str(i + 1) for i, cell in enumerate(board)]
    print(f"\n {labels[0]} | {labels[1]} | {labels[2]} ")
    print("---+---+---")
    print(f" {labels[3]} | {labels[4]} | {labels[5]} ")
    print("---+---+---")
    print(f" {labels[6]} | {labels[7]} | {labels[8]} \n")


def score_terminal(result: str, depth: int) -> int:
    if result == "O":
        return 10 - depth
    if result == "X":
        return depth - 10
    return 0


def minimax(board: Board, maximizing: bool, alpha: int, beta: int, depth: int) -> int:
    result = winner(board)
    if result:
        return score_terminal(result, depth)

    if maximizing:
        best = -inf
        for i, cell in enumerate(board):
            if cell == " ":
                board[i] = "O"
                best = max(best, minimax(board, False, alpha, beta, depth + 1))
                board[i] = " "
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return int(best)

    best = inf
    for i, cell in enumerate(board):
        if cell == " ":
            board[i] = "X"
            best = min(best, minimax(board, True, alpha, beta, depth + 1))
            board[i] = " "
            beta = min(beta, best)
            if beta <= alpha:
                break
    return int(best)


def best_move(board: Board) -> int:
    move = -1
    best = -inf
    for i, cell in enumerate(board):
        if cell == " ":
            board[i] = "O"
            value = minimax(board, False, -inf, inf, 0)
            board[i] = " "
            if value > best:
                best = value
                move = i
    return move


def read_player_move(board: Board) -> int:
    while True:
        raw = input("Choose a cell (1-9): ").strip()
        if raw.isdigit():
            move = int(raw) - 1
            if 0 <= move < 9 and board[move] == " ":
                return move
        print("Invalid move. Pick an empty cell from 1 to 9.")


def main() -> None:
    board = [" "] * 9
    print("Tic Tac Toe: You are X, AI is O.")

    while not winner(board):
        render(board)
        board[read_player_move(board)] = "X"
        if winner(board):
            break
        ai_move = best_move(board)
        board[ai_move] = "O"
        print(f"AI chose cell {ai_move + 1}.")

    render(board)
    result = winner(board)
    if result == "draw":
        print("Draw. The AI held the line.")
    else:
        print(f"{result} wins!")


if __name__ == "__main__":
    main()
