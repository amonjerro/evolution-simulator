import os
from PIL import Image, ImageDraw

class ImageManager:
    def __init__(self, cnfg):
        self.output_path = cnfg['image-output-path']
        self.being_size = cnfg['being-size']
        self.image_size = (cnfg['board-size']*self.being_size, cnfg['board-size']*self.being_size)

        if self.output_path not in [fo.name for fo in os.scandir()]:
            os.mkdir(f'./{self.output_path}')

    def render_simulation_step(self, step, beings):
        im = Image.new("RGB", self.image_size, (255,255,255))
        draw = ImageDraw.Draw(im)
        for being in beings:
            self.draw_being(draw, being)
        with open(f'./{self.output_path}/simulation_step_{step}.jpg', 'wb') as f:
            im.save(f, 'jpeg')

    def draw_being(self, draw_ctx, being):
        origin_x = being.x * self.being_size
        origin_y = being.y * self.being_size
        draw_ctx.ellipse(
            [
                (origin_x, origin_y),
                (origin_x+self.being_size, origin_y+self.being_size)
            ],
            being.genome.genes_to_color()
            )
