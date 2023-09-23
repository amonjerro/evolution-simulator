import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from src.Reports import performance
from src.Reports.performance import performance_check

from src.neuron import NeuronFactory


class ImageManagerSingleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ImageManagerSingleton, cls).__new__(cls)
        return cls.instance
    
    def config(self, config):
        self.MAX_GIF_DURATION = 2000
        self.output_path = config['image-output-path']
        self.being_size = config['being-size']
        self.image_size = (config['board-size']*self.being_size, config['board-size']*self.being_size)
        self.image_by_step = config['image-by-step']
        self.frames = []
        self.draw_selection = None
        if self.output_path not in [fo.name for fo in os.scandir()]:
            os.mkdir(f'./{self.output_path}')
        if 'gen_gifs' not in [i.name for i in os.scandir(f'./{self.output_path}')]:
            os.mkdir(f'./{self.output_path}/gen_gifs')
        if self.image_by_step and 'sim_steps' not in [i.name for i in os.scandir(f'./{self.output_path}')]:
            os.mkdir(f'./{self.output_path}/sim_steps') 

    @performance_check('render_step', "Render a simulation step", "sim_step")
    def render_simulation_step(self, gen, step, beings):
        im = Image.new("RGB", self.image_size, (255,255,255, 255))
        draw = ImageDraw.Draw(im, 'RGBA')
        for being in beings:
            self.draw_being(draw, being)
        
        self.frames.append(im)

        #Conditional image rendering
        if self.image_by_step:
            with open(f'./{self.output_path}/sim_steps/simulation_step_{gen}-{step}.jpg', 'wb') as f:
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
    
    def draw_box_filter(self, rect):
        for f in self.frames:
            draw = ImageDraw.Draw(f, 'RGBA')
            draw.rectangle((
                rect.x1 * self.being_size,
                rect.y1 * self.being_size,
                rect.x2 * self.being_size,
                rect.y2 * self.being_size
            ),
            fill=(125,0,0,60))
    
    def draw_circle_filter(self, circle):
        for f in self.frames:
            draw = ImageDraw.Draw(f, 'RGBA')
            draw.ellipse([
                (circle.x * self.being_size, circle.y * self.being_size),
                (
                    circle.x * self.being_size + circle.r * self.being_size,
                    circle.y * self.being_size + circle.r * self.being_size
                )
            ],
            fill=(125, 0, 0, 60))

    @performance_check('create_gif', "Turn the images into a gif", "sim_step")
    def make_gif_from_gen(self, gen):
        self.frames[0].save(
            f'./{self.output_path}/gen_gifs/generation_{gen}.gif',
            save_all=True,
            append_images=self.frames[1:],
            duration=(self.MAX_GIF_DURATION/len(self.frames)),
            loop=0
            )
        del self.frames[:]

    def display_genome(self, being, index):
        plt.clf()
        nFac = NeuronFactory()
        neuron_digraph = nFac.make_neuron_graph()
        neuron_position_spec, color_map = nFac.decorate_neurons_for_drawing()
        genome = being.get_genome()
        for gene in genome.genes:
            origin, target, sensitivity = gene.decode(genome.blueprints)
            neuron_digraph.add_edge(origin.name, target.name, weight=sensitivity)
        nx.draw_networkx(neuron_digraph, neuron_position_spec, node_color=color_map, node_size=50, font_size=8)
        plt.title(str(being.get_genome()))
        plt.savefig(f'./{self.output_path}/reports/being{index}_network.png')
