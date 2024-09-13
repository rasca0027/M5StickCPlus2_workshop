from M5 import BtnPWR, BtnB, Widgets
from time import ticks_cpu
from machine import Timer
from random import randint, seed


class Food:
    pos = [0, 0]
    def generate():
        Food.pos = [randint(2, 157), randint(2, 77)]
        Food.pos = [Food.pos[0] if Food.pos[0] %2 == 0 else Food.pos[0] - 1, Food.pos[1] if Food.pos[1] % 2 == 0 else Food.pos[1] - 1]
        Food.checkPosition()
        
    def checkPosition():
        while Snake.tail.count(Food.pos) > 0:
            Food.generate()
 
class Snake:
    move_r = [2, 0]
    move_l = [-2,0]
    move_u = [0,-2]
    move_d = [0, 2]
    moves = [move_u, move_r, move_d, move_l]
    dr = 1 #direction
    tail = [[44, 44], [42, 44], [40, 44]]
    timer = Timer(58463)
    speed = 500
    notail = [2,2]
    isDead = False
    def isAlive(head):
        return head[0] > 0 and head[0] < 158 and head[1] > 0 and head[1] < 78 and Snake.tail.count(head) == 0
    
    def run():
        seed(ticks_cpu())
        Widgets.setRotation(1)
        Snake.timer.init(period=Snake.speed, mode=Timer.PERIODIC, callback=Snake.move)
        
    def dirChange():
        if BtnB.isPressed():
            Snake.dr += 1
        if BtnPWR.isPressed():
            Snake.dr -= 1
        if Snake.dr > 3:
            Snake.dr = 0
        if Snake.dr < 0:
            Snake.dr = 3
            
    def reset():
        Snake.isDead = False
        Snake.tail = [[44, 44], [42, 44], [40, 44]]
        Snake.notail = [2,2]
        Snake.dr = 1
        Snake.speed = 500
        
    def speedUp():
        Snake.speed = Snake.speed - 20 if Snake.speed > 140 else 140
        Snake.timer.init(period=Snake.speed, mode=Timer.PERIODIC, callback=Snake.move)
        
    def move(tmr=None):
        head = Snake.tail[0].copy()
        Snake.dirChange()
        #Snake.basicAIMove(head) #uncomment this line if you want AI to play Snake
        head[0] += Snake.moves[Snake.dr][0]
        head[1] += Snake.moves[Snake.dr][1]
        if [head].count(Food.pos) == 0:
            Snake.notail = Snake.tail.pop() 
        else:
            Food.generate()
            Snake.speedUp()
        Snake.isDead = not Snake.isAlive(head)
        Snake.tail.insert(0, head)
        
    def basicAIMove(head):
        if head[0] == Food.pos[0]:
            Snake.dr = 2 if Food.pos[1] > head[1] and Snake.dr != 0 else 0 if Snake.dr !=2 else Snake.dr
        if head[1] == Food.pos[1]:
            Snake.dr = 1 if Food.pos[0] > head[0] and Snake.dr != 3 else 3 if Snake.dr !=1 else Snake.dr
        if (head[0] > 155 and Snake.dr == 1) or (head[0] < 3 and Snake.dr == 3):
            print(head[0])
            Snake.dr = 0 if head[1] > Food.pos[1] else 2
        if (head[1] > 75 and Snake.dr == 2) or (head[1] < 4 and Snake.dr == 0):
            Snake.dr = 3 if head[0] > Food.pos[0] else 1

class Game:
    def drawBorders():
        rect0 = Widgets.Rectangle(0, 0, 160, 80)
        
    def prepareField():
        Snake.run()
        Widgets.fillScreen(0x000000)
        Game.drawBorders()
        Food.generate()
        
    def loop():
        # render snake
        for tailpart in Snake.tail:
            Widgets.Rectangle(tailpart[0], tailpart[1], 2, 2)
        # clear old tail coords
        Widgets.Rectangle(Snake.notail[0], Snake.notail[1], 2, 2, 0)
        # render food
        Widgets.Rectangle(Food.pos[0], Food.pos[1], 2, 2, 0x00ff00)
        return not Snake.isDead
    
    def over():
        Snake.timer.deinit()
        Widgets.fillScreen(0x100000)
        game_over_text = Widgets.Label("GAME OVER", 20, 20, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        score = repr(len(Snake.tail))
        score_label = Widgets.Label(f"score: {score}", 40, 40, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

        while BtnPWR.isPressed():
            pass
        while True:
            if BtnPWR.isPressed():
                Snake.reset()
                Game.prepareField()
                return 0

Game.prepareField()
while True:
    Game.loop() or Game.over()
