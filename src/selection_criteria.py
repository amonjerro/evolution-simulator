from src.Reports.performance import performance_check
from src.being import PopulationSingleton

@performance_check("filter", "Apply selection filter", "sim_step")
def box_filter(rect):
    beings = PopulationSingleton().get_beings()
    survivors = [ b for b in beings if b.position.x >= rect.x1 and b.position.x <= rect.x2 and b.position.y >= rect.y1 and b.position.y <= rect.y2 ]
    return survivors

def circle_filter(circle):
    beings = PopulationSingleton().get_beings()
    survivors = [ b for b in beings if (b.position.x-circle.x)**2+(b.position.y-circle.y)**2 <= circle.r**2]
    return survivors
