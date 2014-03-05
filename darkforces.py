from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Rectangle
from random import randint

class physicalObject:
    velocity_x= NumericProperty(0)
    velocity_y= NumericProperty(0)
    velocity= ReferenceListProperty(velocity_x, velocity_y)

    acceleration_x= NumericProperty(0)
    acceleration_y= NumericProperty(0)
    acceleration= ReferenceListProperty(acceleration_x, acceleration_y)

    collisionDir = [1,1,1,1]

class Player(Widget, physicalObject):
    position = [0,0]
    def move(self, dt):
        self.velocity_x += self.acceleration_x*dt - self.velocity_x*.01
        #friction from the ground
        if self.collisionDir[3] < 1:
            self.velocity_x -= self.velocity_x*.05 
        if (self.velocity_x < 0 and self.collisionDir[1] == 0) or (self.velocity_x > 0 and self.collisionDir[2] == 0):
            self.velocity_x = 0

        self.velocity_y += self.acceleration_y*dt - 9.81*dt - self.velocity_y*.01
        if (self.velocity_y > 0 and self.collisionDir[2] == 0) or (self.velocity_y < 0 and self.collisionDir[3] == 0):
            self.velocity_y = 0

        self.position = self.velocity + self.position

class GroundBlock(Widget, physicalObject):
    def __init__(self, pos_x, pos_y, **kwargs):
        super(GroundBlock, self).__init__(**kwargs)
        with self.canvas:
            self.pos = pos_x, pos_y 
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)

    def checkCollision(self, widgetAndphyObj):
        horz =  self.pos[0] - widgetAndphyObj.pos[0]  
        vert =  self.pos[1] - widgetAndphyObj.pos[1]
        #      Left  Right Up    Down
        col = [False,False,False,False]
        if horz > 0 and self.width > abs(horz):
            col[0] = True
        elif horz < 0 and widgetAndphyObj.width > abs(horz):
            col[0] = True

        if vert < 0 and self.height > abs(vert):
            col[1] = True
        elif vert > 0 and widgetAndphyObj.height > abs(vert):
            col[1] = True


        if col[0] and col[1]:
            widgetAndphyObj.collisionDir[3] = 0 

    def move(self, camera):
        self.pos = Vector([self.pos[0] - camera[0], self.pos[1] - camera[1]])


class DarkforcesGame(Widget):
    player = ObjectProperty(None)
    ground = list() 
    camera = [0,0]


    def __init__(self, **kwargs):
        super(DarkforcesGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        #self.ground[0].pos = Vector(self.ground.pos) + Vector(self.player.pos)
        self.generateFloor()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)
        player = self.player
        if keycode[1] in 'wasd':
            if keycode[1] == 'w':# and player.pos <= Vector(20.0, 20.0):
                if player.collisionDir[3] == 0:
                    player.velocity_y += 10
                elif player.velocity_y <= -2:
                    player.velocity_y += 2
            if keycode[1] == 'a' and player.velocity_y == 0:
                player.velocity_x += -3
            if keycode[1] == 'd' and player.velocity_y == 0:
                player.velocity_x += 3

    def update(self, dt):
        self.player.collisionDir = [1,1,1,1]
        self.camera = self.player.position
        
        for i in self.ground:
            i.checkCollision(self.player)
            i.move(self.camera)
        self.player.move(dt) 

    def generateFloor(self):
        for i in range(100):
            self.ground.append(GroundBlock(i*32,0))
            self.add_widget(self.ground[i])
    
class DarkforcesApp(App):
    def build(self):
        game = DarkforcesGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    DarkforcesApp().run()

