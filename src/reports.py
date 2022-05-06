import os
import matplotlib.pyplot as plt

class ReportSingleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ReportSingleton, cls).__new__(cls)
        return cls.instance        
    def config(self, config):
        self.generation_deaths = []
        self.generation_diversity = []
        self.output_path = config['image-output-path']
        if 'reports' not in [i.name for i in os.scandir(f'./{self.output_path}')]:
            os.mkdir(f'./{self.output_path}/reports') 
    def add_generation_data(self, generation_deaths, generation_diversity):
        self.generation_deaths.append(generation_deaths)
        self.generation_diversity.append(generation_diversity)
    def plot_death_rate(self):
        plt.title('Deaths by Generation')
        plt.plot(
            [i for i in range(len(self.generation_deaths))], 
            self.generation_deaths 
        )
        plt.savefig(f'./{self.output_path}/reports/death_rate_by_gen.png')
    def get_death_rate(self, index):
        return self.generation_deaths[index]
