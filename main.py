import time
import turtle as tr
from paddle import Paddle
from ball import Ball
from score import Score
from ui import UI
from bricks import Bricks

screen = tr.Screen()
paddle = Paddle()
bricks = Bricks()
ball = Ball()
score = Score(lives=5)

game = True
paused = False


def pause_game():
	global paused
	if paused:
		paused = False
	else:
		paused = True


screen.setup(width=1200, height=600)
screen.bgcolor('black')
screen.title('Breakout')
screen.tracer(0)

ui = UI()
ui.header()

screen.listen()
screen.onkey(key='Left', fun=paddle.move_left)
screen.onkey(key='Right', fun=paddle.move_right)
screen.onkey(key='space', fun=pause_game)


def check_collision_walls():
	global ball, score, game, ui
	# проверяем коллизию от стены справа и слева
	if ball.xcor() < -580 or ball.xcor() > 570:
		ball.bounce(x_bounce=True, y_bounce=False)
		return

	# проверяем коллизию от стены сверху
	if ball.ycor() > 270:
		ball.bounce(x_bounce=False, y_bounce=True)
		return

	# проверяем коллизию от стены снизу, если мяч ее коснется то игра перезапускается
	if ball.ycor() < -280:
		ball.reset()
		score.decrease_lives()
		if score.lives == 0:
			score.reset()
			game = False
			ui.game_over(win=False)
			return
		ui.change_color()
		return


def check_collision_paddle():
	global ball, paddle
	# записываем координаты мяча и платформы по Х
	paddle_x = paddle.xcor()
	ball_x = ball.xcor()

	if ball.distance(paddle) < 110 and ball.ycor() < -250:

		# если платформа справа от экрана
		if paddle_x > 0:
			if ball_x > paddle_x:
				# если мяч бьет в ракету слева, он должен вернутся налево
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return

		# если платформа слева от экрана
		elif paddle_x < 0:
			if ball_x < paddle_x:
				# если мяч бьет в ракету слева, он должен вернутся налево
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return

		# остальное для положения по середине
		else:
			if ball_x > paddle_x:
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			elif ball_x < paddle_x:
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return


def check_collision_bricks():
	global ball, bricks, score

	for brick in bricks.bricks:
		if ball.distance(brick) < 40:
			score.increase_score()
			brick.quantity -= 1
			if brick.quantity == 0:
				brick.clear()
				brick.goto(3000, 3000)
				bricks.bricks.remove(brick)

			# касание слева
			if ball.xcor() < brick.left_wall:
				ball.bounce(x_bounce=True, y_bounce=False)

			# касание справа
			elif ball.xcor() > brick.right_wall:
				ball.bounce(x_bounce=True, y_bounce=False)

			# касание снизу
			elif ball.ycor() < brick.bottom_wall:
				ball.bounce(x_bounce=False, y_bounce=True)

			# касание сверху
			elif ball.ycor() > brick.upper_wall:
				ball.bounce(x_bounce=False, y_bounce=True)


while game:
	if not paused:

		# обновление экрана
		screen.update()
		time.sleep(0.01)
		ball.move()

		check_collision_walls()

		check_collision_paddle()

		check_collision_bricks()

		# победа
		if len(bricks.bricks) == 0:
			ui.game_over(win=True)
			break

	else:
		ui.paused_status()

tr.mainloop()
