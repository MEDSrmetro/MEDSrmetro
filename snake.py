import curses
import random


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    height, width = stdscr.getmaxyx()

    snake = [[height // 2, width // 2 + i] for i in range(3)]
    direction = curses.KEY_LEFT

    food = [random.randint(1, height - 2), random.randint(1, width - 2)]
    stdscr.addch(food[0], food[1], curses.ACS_PI)

    score = 0

    while True:
        key = stdscr.getch()
        if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            opposite = {
                curses.KEY_UP: curses.KEY_DOWN,
                curses.KEY_DOWN: curses.KEY_UP,
                curses.KEY_LEFT: curses.KEY_RIGHT,
                curses.KEY_RIGHT: curses.KEY_LEFT,
            }
            if key != opposite.get(direction):
                direction = key
        elif key == ord('q'):
            break

        head = snake[0][:]
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        snake.insert(0, head)

        if (
            head[0] in (0, height - 1)
            or head[1] in (0, width - 1)
            or head in snake[1:]
        ):
            break

        if head == food:
            score += 1
            food = None
            while food is None:
                new_food = [random.randint(1, height - 2), random.randint(1, width - 2)]
                if new_food not in snake:
                    food = new_food
            stdscr.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        stdscr.addch(head[0], head[1], curses.ACS_CKBOARD)
        stdscr.addstr(0, 0, f"Score: {score}")

    curses.endwin()
    print(f"Game over! Final score: {score}")


if __name__ == "__main__":
    curses.wrapper(main)
