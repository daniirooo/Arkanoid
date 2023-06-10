import tkinter
import random
from tkinter import messagebox
import sys
import os
from tkinter import *

window = tkinter.Tk()
window.title("Меню игры")
window.geometry("360x300")
window.config(bg='gray')
window.resizable(False, False)


new_window = None

def quit_game():
    window.destroy()

def poyasnenie():
    def close_poyasnenye():
        lable1.destroy()
        close_button.destroy()
        poasnenue_button.config(state='normal')

    lable1 = tkinter.Label(text='Основной целью игры является уничтожение всех кирпичиков. \n Управление происходит за счет движения мыши', bg='gray')
    lable1.pack()
    poasnenue_button.config(state='disabled')
    close_button = tkinter.Button(text='Закрыть пояснение', command=close_poyasnenye, width=20)
    close_button.pack(pady=15)

def createnewwindow():
    global paused  # Объявление глобальной переменной paused
    paused = False  # Инициализация переменной в начальное значение

    def close_window():
        new_window.destroy()


    def lvl_easy(WIDTH, HEIGHT):  # Функция создания окна с правила игры
        global x, x1, y, vx, vy, points, game_mode, count
        window.destroy()
        vibor.destroy()
        new_window = tkinter.Toplevel()  # Создание нового окна с использованием Toplevel
        new_window.title("Игра")
        new_window.geometry(f"{WIDTH}x{HEIGHT}")
        new_window.resizable(False, False)  # Запрет изменения размеров окна
        def New_Game():
            message2 = messagebox.askyesno('Новая игра', 'Вы действительно хотите начать новую игру?')
            if message2:
                python = sys.executable
                os.execl(python, python, *sys.argv)

        def Vihod():
            root.destroy()

        def score_up():
            global points
            points += 1
            canvas.itemconfig(score, text=str(points))

        def mouse_move(event):
            global x1
            x1 = event.x
            move_platform_and_score()

        def move_platform_and_score():
            if game_mode and not paused:
                canvas.coords(platform, x1 - PLATFORM_W // 2, HEIGHT, x1 + PLATFORM_W // 2, HEIGHT - PLATFORM_H)
                canvas.coords(score, x1, HEIGHT - PLATFORM_H // 2)

        def get_brick():
            for brick in bricks:
                xb1, yb1, xb2, yb2 = canvas.coords(brick)
                if xb1 < x < xb2 and yb1 < y < yb2:
                    return brick

        WIDTH, HEIGHT = 1200, 500
        x, y = WIDTH // 2, HEIGHT // 2
        vx, vy = -10, -10
        BALL_RADIUS = 20
        TIMEOUT = 40

        x1 = WIDTH // 2
        PLATFORM_H = 50
        PLATFORM_W = 250

        BRICKS_PART = 0.3
        ROWS, COLS = 4, 16

        points = 0
        game_mode = True
        paused_label = None  # Переменная для хранения объекта Label с надписью "Пауза"

        root = tkinter.Tk()

        mainmenu = Menu(root)
        root.config(menu=mainmenu)

        canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
        canvas.pack()

        ball = canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill='yellow')

        platform = canvas.create_rectangle(x1 - PLATFORM_W // 2, HEIGHT, x1 + PLATFORM_W // 2, HEIGHT - PLATFORM_H,
                                           fill='green')

        score = canvas.create_text(x1, HEIGHT - PLATFORM_H // 2, text='0', font=('Courier', 32, 'bold'), fill='white')

        brick_w, brick_h = WIDTH / COLS, HEIGHT * BRICKS_PART / ROWS

        bricks = []

        for row in range(ROWS):
            for col in range(COLS):
                xb, yb = col * brick_w, row * brick_h
                red, green, blue = (random.randint(0, 255) for _ in range(3))
                color = f'#{red:0>2x}{green:0>2x}{blue:0>2x}'
                bricks.append(canvas.create_rectangle(xb, yb, xb + brick_w, yb + brick_h, fill=color))

        def game():
            global x, y, vx, vy, points, game_mode, count, paused, paused_label
            x, y = vx + x, vy + y
            canvas.coords(ball, x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS)
            if y <= BALL_RADIUS:
                vy = abs(vy)
            if x <= BALL_RADIUS or x >= WIDTH - BALL_RADIUS:
                vx = -vx

            if x1 - PLATFORM_W // 2 <= x <= x1 + PLATFORM_W // 2 and \
                    y == HEIGHT - (BALL_RADIUS + PLATFORM_H):
                vy = -vy

            brick = get_brick()

            if brick:
                vy = -vy
                canvas.delete(brick)
                bricks.pop(bricks.index(brick))
                score_up()

            root.update()

            if points == 64:
                game_mode = False
                canvas.create_text(WIDTH // 2, HEIGHT // 2, text='Victory', fill='red', font=(None, 50))
                message = messagebox.askyesno(title='Победа', message='Хотите начать новую игру?')
                if message:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                else:
                    root.destroy()

            if y < (HEIGHT - BALL_RADIUS) and not paused:
                root.after(TIMEOUT, game)
            elif not paused:
                game_mode = False
                canvas.create_text(WIDTH // 2, HEIGHT // 2, text='GAME OVER', fill='red', font=(None, 50))
                message = messagebox.askyesno(title='Поражение', message='Хотите начать новую игру?')
                if message:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                else:
                    root.destroy()

            elif paused:
                if not paused_label:  # Если надписи "Пауза" нет, создаем ее
                    paused_label = canvas.create_text(WIDTH // 2, HEIGHT // 2, text='Пауза', fill='red',
                                                      font=(None, 50))

        def pause_game():
            global paused
            paused = not paused
            if not paused:
                canvas.delete(paused_label)  # Удаляем надпись "Пауза"
                game()

        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Новая игра", command=New_Game)

        mainmenu.add_cascade(label="Игра",
                             menu=filemenu)

        pause_button = tkinter.Button(root, text='Пауза', command=pause_game)
        pause_button.pack()

        game()
        canvas.bind('<Motion>', mouse_move)
        root.mainloop()

    def lvl_medium ():  # Функция создания окна с правила игры
        global x, x1, y, vx, vy, points, game_mode, count
        window.destroy()
        vibor.destroy()

        def New_Game():
            message2 = messagebox.askyesno('Новая игра', 'Вы действительно хотите начать новую игру?')
            if message2:
                python = sys.executable
                os.execl(python, python, *sys.argv)

        def Vihod():
            root.destroy()

        def score_up():
            global points
            points += 1
            canvas.itemconfig(score, text=str(points))

        def mouse_move(event):
            global x1
            x1 = event.x
            move_platform_and_score()

        def move_platform_and_score():
            if game_mode and not paused:
                canvas.coords(platform, x1 - PLATFORM_W // 2, HEIGHT, x1 + PLATFORM_W // 2, HEIGHT - PLATFORM_H)
                canvas.coords(score, x1, HEIGHT - PLATFORM_H // 2)

        def get_brick():
            for brick in bricks:
                xb1, yb1, xb2, yb2 = canvas.coords(brick)
                if xb1 < x < xb2 and yb1 < y < yb2:
                    return brick

        WIDTH, HEIGHT = 1200, 500
        x, y = WIDTH // 2, HEIGHT // 2
        vx, vy = -10, -10
        BALL_RADIUS = 20
        TIMEOUT = 50

        x1 = WIDTH // 2
        PLATFORM_H = 50
        PLATFORM_W = 250

        BRICKS_PART = 0.3
        ROWS, COLS = 4, 16

        points = 0
        game_mode = True
        paused_label = None  # Переменная для хранения объекта Label с надписью "Пауза"

        root = tkinter.Tk()

        mainmenu = Menu(root)
        root.config(menu=mainmenu)

        canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
        canvas.pack()

        ball = canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill='yellow')

        platform = canvas.create_rectangle(x1 - PLATFORM_W // 2, HEIGHT, x1 + PLATFORM_W // 2, HEIGHT - PLATFORM_H,
                                           fill='green')

        score = canvas.create_text(x1, HEIGHT - PLATFORM_H // 2, text='0', font=('Courier', 32, 'bold'), fill='white')

        brick_w, brick_h = WIDTH / COLS, HEIGHT * BRICKS_PART / ROWS

        bricks = []

        for row in range(ROWS):
            for col in range(COLS):
                xb, yb = col * brick_w, row * brick_h
                red, green, blue = (random.randint(0, 255) for _ in range(3))
                color = f'#{red:0>2x}{green:0>2x}{blue:0>2x}'
                bricks.append(canvas.create_rectangle(xb, yb, xb + brick_w, yb + brick_h, fill=color))

        def game():
            global x, y, vx, vy, points, game_mode, count, paused, paused_label
            x, y = vx + x, vy + y
            canvas.coords(ball, x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS)
            if y <= BALL_RADIUS:
                vy = abs(vy)
            if x <= BALL_RADIUS or x >= WIDTH - BALL_RADIUS:
                vx = -vx

            if x1 - PLATFORM_W // 2 <= x <= x1 + PLATFORM_W // 2 and \
                    y == HEIGHT - (BALL_RADIUS + PLATFORM_H):
                vy = -vy

            brick = get_brick()

            if brick:
                vy = -vy
                canvas.delete(brick)
                bricks.pop(bricks.index(brick))
                score_up()

            root.update()

            if points == 64:
                game_mode = False
                canvas.create_text(WIDTH // 2, HEIGHT // 2, text='Victory', fill='red', font=(None, 50))
                message = messagebox.askyesno(title='Победа', message='Хотите начать новую игру?')
                if message:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                else:
                    root.destroy()

            if y < (HEIGHT - BALL_RADIUS) and not paused:
                root.after(TIMEOUT, game)
            elif not paused:
                game_mode = False
                canvas.create_text(WIDTH // 2, HEIGHT // 2, text='GAME OVER', fill='red', font=(None, 50))
                message = messagebox.askyesno(title='Поражение', message='Хотите начать новую игру?')
                if message:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                else:
                    root.destroy()

            elif paused:
                if not paused_label:  # Если надписи "Пауза" нет, создаем ее
                    paused_label = canvas.create_text(WIDTH // 2, HEIGHT // 2, text='Пауза', fill='red',
                                                      font=(None, 50))

        def pause_game():
            global paused
            paused = not paused
            if not paused:
                canvas.delete(paused_label)  # Удаляем надпись "Пауза"
                game()

        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Новая игра", command=New_Game)

        mainmenu.add_cascade(label="Игра",
                             menu=filemenu)

        pause_button = tkinter.Button(root, text='Пауза', command=pause_game)
        pause_button.pack()

        game()
        canvas.bind('<Motion>', mouse_move)
        root.mainloop()

    def lvl_hard():  # Функция создания окна с правила игры
        global x, x1, y, vx, vy, points, game_mode, count
        window.destroy()
        vibor.destroy()

        def New_Game():
            message2 = messagebox.askyesno('Новая игра', 'Вы действительно хотите начать новую игру?')
            if message2:
                python = sys.executable
                os.execl(python, python, *sys.argv)

        def Vihod():
            root.destroy()

        def score_up():
            global points
            points += 1
            canvas.itemconfig(score, text=str(points))

        def mouse_move(event):
            global x1
            x1 = event.x
            move_platform_and_score()

        def move_platform_and_score():
            if game_mode and not paused:
                canvas.coords(platform, x1 - PLATFORM_W // 2, HEIGHT, x1 + PLATFORM_W // 2, HEIGHT - PLATFORM_H)
                canvas.coords(score, x1, HEIGHT - PLATFORM_H // 2)

        def get_brick():
            for brick in bricks:
                xb1, yb1, xb2, yb2 = canvas.coords(brick)
                if xb1 < x < xb2 and yb1 < y < yb2:
                    return brick

        WIDTH, HEIGHT = 1200, 500
        x, y = WIDTH // 2, HEIGHT // 2
        vx, vy = -10, -10
        BALL_RADIUS = 20
        TIMEOUT = 20

        x1 = WIDTH // 2
        PLATFORM_H = 50
        PLATFORM_W = 250

        BRICKS_PART = 0.3
        ROWS, COLS = 4, 16

        points = 0
        game_mode = True
        paused_label = None  # Переменная для хранения объекта Label с надписью "Пауза"

        root = tkinter.Tk()

        mainmenu = Menu(root)
        root.config(menu=mainmenu)

        canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
        canvas.pack()

        ball = canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill='yellow')

        platform = canvas.create_rectangle(x1 - PLATFORM_W // 2, HEIGHT, x1 + PLATFORM_W // 2, HEIGHT - PLATFORM_H,
                                           fill='green')

        score = canvas.create_text(x1, HEIGHT - PLATFORM_H // 2, text='0', font=('Courier', 32, 'bold'), fill='white')

        brick_w, brick_h = WIDTH / COLS, HEIGHT * BRICKS_PART / ROWS

        bricks = []

        for row in range(ROWS):
            for col in range(COLS):
                xb, yb = col * brick_w, row * brick_h
                red, green, blue = (random.randint(0, 255) for _ in range(3))
                color = f'#{red:0>2x}{green:0>2x}{blue:0>2x}'
                bricks.append(canvas.create_rectangle(xb, yb, xb + brick_w, yb + brick_h, fill=color))

        def game():
            global x, y, vx, vy, points, game_mode, count, paused, paused_label
            x, y = vx + x, vy + y
            canvas.coords(ball, x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS)
            if y <= BALL_RADIUS:
                vy = abs(vy)
            if x <= BALL_RADIUS or x >= WIDTH - BALL_RADIUS:
                vx = -vx

            if x1 - PLATFORM_W // 2 <= x <= x1 + PLATFORM_W // 2 and \
                    y == HEIGHT - (BALL_RADIUS + PLATFORM_H):
                vy = -vy

            brick = get_brick()

            if brick:
                vy = -vy
                canvas.delete(brick)
                bricks.pop(bricks.index(brick))
                score_up()

            root.update()

            if points == 64:
                game_mode = False
                canvas.create_text(WIDTH // 2, HEIGHT // 2, text='Victory', fill='red', font=(None, 50))
                message = messagebox.askyesno(title='Победа', message='Хотите начать новую игру?')
                if message:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                else:
                    root.destroy()

            if y < (HEIGHT - BALL_RADIUS) and not paused:
                root.after(TIMEOUT, game)
            elif not paused:
                game_mode = False
                canvas.create_text(WIDTH // 2, HEIGHT // 2, text='GAME OVER', fill='red', font=(None, 50))
                message = messagebox.askyesno(title='Поражение', message='Хотите начать новую игру?')
                if message:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                else:
                    root.destroy()

            elif paused:
                if not paused_label:  # Если надписи "Пауза" нет, создаем ее
                    paused_label = canvas.create_text(WIDTH // 2, HEIGHT // 2, text='Пауза', fill='red',
                                                      font=(None, 50))

        def pause_game():
            global paused
            paused = not paused
            if not paused:
                canvas.delete(paused_label)  # Удаляем надпись "Пауза"
                game()

        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Новая игра", command=New_Game)

        mainmenu.add_cascade(label="Игра",
                             menu=filemenu)

        pause_button = tkinter.Button(root, text='Пауза', command=pause_game)
        pause_button.pack()

        game()
        canvas.bind('<Motion>', mouse_move)
        root.mainloop()

    def quit_vibor():
        vibor.destroy()

    vibor = tkinter.Tk()
    vibor.geometry('300x250')
    vibor.config(bg='gray')
    easy_button = tkinter.Button(vibor, text="Легкий уровень", command=lvl_easy, width=20)
    easy_button.pack(pady=15)

    medium_button = tkinter.Button(vibor, text="Средний уровень", command=lvl_medium, width=20)
    medium_button.pack(pady=15)

    hard_button = tkinter.Button(vibor, text="Сложный уровень", command=lvl_hard, width=20)
    hard_button.pack(pady=15)

    back_button = tkinter.Button(vibor, text="Вернуться в главное меню", command=quit_vibor, width=20)
    back_button.pack(pady=15)

    vibor.mainloop()

start_button = tkinter.Button(text="Начать игру", command=createnewwindow, width=20)
start_button.pack(pady=15)

quit_button = tkinter.Button(text="Выйти из игры", command=quit_game, width=20)
quit_button.pack(pady=15)

poasnenue_button = tkinter.Button(text="Открыть пояснение", command=poyasnenie, width=20)
poasnenue_button.pack(pady=15)

window.mainloop()
