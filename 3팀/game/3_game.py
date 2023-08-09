from ursina import *
#from ursina.prefabs import Button
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.fps_counter.enabled = False  # 우측 위 숫자 지우기
window.exit_button.visible = False  # X버튼 지우기

sand = Audio('sand.mp3', autoplay = False)
punch = Audio('punch.mp3', autoplay = False)
lava = Audio('lava.mp3', autoplay = False)

blocks = [
    load_texture('grass.png'), # 0
    load_texture('grass.png'), # 1
    load_texture('stone.png'), # 2
    load_texture('lava.png'), # 3
    load_texture('gold.png'), # 4
    load_texture('sand.png'), # 5
    load_texture('wood.png') # 6
]

block_id = 1
def input(key): # 키보드
    if key.isdigit():
        global block_id, hand
        block_id = int(key)

        if block_id >= len(blocks):  # 6 이상의 숫자가 입력되면, 6이 입력된 것으로 수정
            block_id = len(blocks) -1
        
        hand.texture = blocks[block_id]
 

sky = Entity(
    parent = scene,
    model = 'sphere',
    texture = 'sky.jpg',
    scale = 500,
    double_sided = True
)

hand = Entity(
    parent = camera.ui,
    model = 'block',
    texture = blocks[block_id],
    scale = 0.2,
    rotation = Vec3(-10, -10, 10),
    position = Vec2(0.6, -0.6)
)

def update():
    if held_keys['left mouse'] or held_keys['right_mouse']:
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture = 'grass.png'):  # texture = brick
        super().__init__(
            parent = scene,
            position = position,
            model = 'block', #'cube',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9, 1.0)), # HSV (색조, 채도, 명도)
            # random.uniform(a,b) = [a,b] 사이에 실수형 난수를 발생시킨다
            scale = 0.5
        )
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                Voxel(position= self.position + mouse.normal, texture = blocks[block_id])
                if block_id ==1 or block_id == 5:
                    sand.play()
                elif block_id == 3 :
                    lava.play() 
                else: punch.play()
            elif key == 'right mouse down':
                destroy(self)


for z in range(20):  # 서있을 블록들을 지정. 20*20 크기
    for x in range(20):
        voxel = Voxel(position = (x,0,z))

player = FirstPersonController()  # player를 만들어줌. player의 시점에서 볼 수 있게 됨!

app.run()