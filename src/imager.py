import os
from PIL import Image, ImageDraw

class ImageManager:
    def __init__(self, cnfg):
        self.MAX_GIF_DURATION = 2000
        self.output_path = cnfg['image-output-path']
        self.being_size = cnfg['being-size']
        self.image_size = (cnfg['board-size']*self.being_size, cnfg['board-size']*self.being_size)
        self.image_by_step = cnfg['image-by-step']
        self.frames = []
        if self.output_path not in [fo.name for fo in os.scandir()]:
            os.mkdir(f'./{self.output_path}')
        

    def render_simulation_step(self, gen, step, beings):
        im = Image.new("RGB", self.image_size, (255,255,255))
        draw = ImageDraw.Draw(im)
        for being in beings:
            self.draw_being(draw, being)
        self.frames.append(im)

        #Conditional image rendering
        if self.image_by_step:
            with open(f'./{self.output_path}/simulation_step_{gen}-{step}.jpg', 'wb') as f:
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

    def gen_to_gif(self, gen):
        self.frames[0].save(
            f'./{self.output_path}/generation_{gen}.gif',
            save_all=True,
            append_images=self.frames[1:],
            duration=(self.MAX_GIF_DURATION/len(self.frames)),
            loop=0
            )
        del self.frames[:]