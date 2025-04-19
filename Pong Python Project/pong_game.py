# pong_game.py
import turtle
import random
import time

class PongGame:
    def __init__(self):
        # Game window setup
        self.win = turtle.Screen()
        self.win.title("Pong Game by Saira")
        self.win.bgcolor("black")
        self.win.setup(width=800, height=600)
        self.win.tracer(0)
        
        # Game state variables
        self.score_a = 0
        self.score_b = 0
        self.game_paused = False
        self.ball_speed_increase = 1.1
        self.max_speed = 0.7
        self.game_over = False
        self.winning_score = 5
        
        # Initialize game components
        self.create_paddles()
        self.create_ball()
        self.create_scoreboard()
        self.create_divider()
        
        # Set up controls
        self.setup_controls()
        
    def create_paddles(self):
        # Paddle A (Left)
        self.paddle_a = turtle.Turtle()
        self.paddle_a.speed(0)
        self.paddle_a.shape("square")
        self.paddle_a.color("deep pink")
        self.paddle_a.shapesize(stretch_wid=6, stretch_len=1)
        self.paddle_a.penup()
        self.paddle_a.goto(-350, 0)
        
        # Paddle B (Right)
        self.paddle_b = turtle.Turtle()
        self.paddle_b.speed(0)
        self.paddle_b.shape("square")
        self.paddle_b.color("cyan")
        self.paddle_b.shapesize(stretch_wid=6, stretch_len=1)
        self.paddle_b.penup()
        self.paddle_b.goto(350, 0)
    
    def create_ball(self):
        # Ball setup
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0, 0)
        self.ball.dx = 0.3
        self.ball.dy = 0.3
        
    def create_scoreboard(self):
        # Score display
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.pen.write("Player A: 0    Player B: 0", align="center", font=("Courier", 24, "normal"))
        
        # Status message
        self.status = turtle.Turtle()
        self.status.speed(0)
        self.status.color("yellow")
        self.status.penup()
        self.status.hideturtle()
        self.status.goto(0, -260)
        self.status.write("Press 'P' to pause, 'R' to reset", align="center", font=("Courier", 16, "normal"))
        
    def create_divider(self):
        # Center divider line
        divider = turtle.Turtle()
        divider.speed(0)
        divider.color("gray")
        divider.penup()
        divider.goto(0, 300)
        divider.pendown()
        divider.setheading(270)
        
        # Draw dashed line
        for _ in range(30):
            divider.forward(10)
            divider.penup()
            divider.forward(10)
            divider.pendown()
        divider.hideturtle()
    
    def paddle_a_up(self):
        if not self.game_paused and not self.game_over:
            y = self.paddle_a.ycor()
            if y < 250:
                self.paddle_a.sety(y + 30)
    
    def paddle_a_down(self):
        if not self.game_paused and not self.game_over:
            y = self.paddle_a.ycor()
            if y > -240:
                self.paddle_a.sety(y - 30)
    
    def paddle_b_up(self):
        if not self.game_paused and not self.game_over:
            y = self.paddle_b.ycor()
            if y < 250:
                self.paddle_b.sety(y + 30)
    
    def paddle_b_down(self):
        if not self.game_paused and not self.game_over:
            y = self.paddle_b.ycor()
            if y > -240:
                self.paddle_b.sety(y - 30)
    
    def toggle_pause(self):
        self.game_paused = not self.game_paused
        if self.game_paused:
            self.status.clear()
            self.status.write("GAME PAUSED - Press 'P' to resume", align="center", font=("Courier", 16, "normal"))
        else:
            self.status.clear()
            self.status.write("Press 'P' to pause, 'R' to reset", align="center", font=("Courier", 16, "normal"))
    
    def reset_game(self):
        # Reset scores
        self.score_a = 0
        self.score_b = 0
        self.update_score()
        
        # Reset ball
        self.ball.goto(0, 0)
        self.ball.dx = 0.3 * random.choice([1, -1])
        self.ball.dy = 0.3 * random.choice([1, -1])
        
        # Reset paddles
        self.paddle_a.goto(-350, 0)
        self.paddle_b.goto(350, 0)
        
        # Reset game state
        self.game_paused = False
        self.game_over = False
        
        # Update status
        self.status.clear()
        self.status.write("Press 'P' to pause, 'R' to reset", align="center", font=("Courier", 16, "normal"))
    
    def update_score(self):
        self.pen.clear()
        self.pen.write(f"Player A: {self.score_a}    Player B: {self.score_b}", align="center", font=("Courier", 24, "normal"))
    
    def setup_controls(self):
        self.win.listen()
        self.win.onkeypress(self.paddle_a_up, "w")
        self.win.onkeypress(self.paddle_a_down, "s")
        self.win.onkeypress(self.paddle_b_up, "Up")
        self.win.onkeypress(self.paddle_b_down, "Down")
        self.win.onkeypress(self.toggle_pause, "p")
        self.win.onkeypress(self.reset_game, "r")
    
    def play_sound(self, sound_type):
        # This is a placeholder for sound effects
        # Actual sound implementation would require additional libraries
        pass
    
    def check_win(self):
        if self.score_a >= self.winning_score:
            self.game_over = True
            self.status.clear()
            self.status.write("Player A wins! Press 'R' to restart", align="center", font=("Courier", 16, "normal"))
            return True
        elif self.score_b >= self.winning_score:
            self.game_over = True
            self.status.clear()
            self.status.write("Player B wins! Press 'R' to restart", align="center", font=("Courier", 16, "normal"))
            return True
        return False
    
    def run(self):
        while True:
            self.win.update()
            
            if self.game_paused or self.game_over:
                continue
                
            # Ball movement
            self.ball.setx(self.ball.xcor() + self.ball.dx)
            self.ball.sety(self.ball.ycor() + self.ball.dy)
            
            # Top and bottom wall bounce
            if self.ball.ycor() > 290:
                self.ball.sety(290)
                self.ball.dy *= -1
                self.play_sound("wall")
            
            if self.ball.ycor() < -290:
                self.ball.sety(-290)
                self.ball.dy *= -1
                self.play_sound("wall")
            
            # Right wall - Player A scores
            if self.ball.xcor() > 390:
                self.ball.goto(0, 0)
                self.ball.dx = abs(self.ball.dx) * -1  # Ensure it goes toward Player A
                self.score_a += 1
                self.update_score()
                self.play_sound("score")
                self.check_win()
                time.sleep(0.5)  # Brief pause after scoring
            
            # Left wall - Player B scores
            if self.ball.xcor() < -390:
                self.ball.goto(0, 0)
                self.ball.dx = abs(self.ball.dx)  # Ensure it goes toward Player B
                self.score_b += 1
                self.update_score()
                self.play_sound("score")
                self.check_win()
                time.sleep(0.5)  # Brief pause after scoring
            
            # Paddle B collision
            if (340 < self.ball.xcor() < 350) and (self.paddle_b.ycor() - 60 < self.ball.ycor() < self.paddle_b.ycor() + 60):
                self.ball.setx(340)
                self.ball.dx *= -1 * min(self.ball_speed_increase, self.max_speed / abs(self.ball.dx))
                self.play_sound("paddle")
                
                # Add slight angle variation based on where the ball hits the paddle
                offset = (self.ball.ycor() - self.paddle_b.ycor()) / 60
                self.ball.dy += offset / 5
            
            # Paddle A collision
            if (-350 < self.ball.xcor() < -340) and (self.paddle_a.ycor() - 60 < self.ball.ycor() < self.paddle_a.ycor() + 60):
                self.ball.setx(-340)
                self.ball.dx *= -1 * min(self.ball_speed_increase, self.max_speed / abs(self.ball.dx))
                self.play_sound("paddle")
                
                # Add slight angle variation based on where the ball hits the paddle
                offset = (self.ball.ycor() - self.paddle_a.ycor()) / 60
                self.ball.dy += offset / 5

if __name__ == "__main__":
    game = PongGame()
    game.run()