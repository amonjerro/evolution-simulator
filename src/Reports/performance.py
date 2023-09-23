import time


class PerformanceInformation:
    def __init__(self, tag='', description='', timeTaken=0):
        self.time = timeTaken
        self.tag = tag
        self.description = description
    def setTimeTaken(self, value):
        self.time = value

class Performance:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Performance, cls).__new__(cls)
        return cls.instance
    
    def config(self):
        self.performance_evaluations = {}
        self.tags = []

    def add_performance_evaluation(self, data):
        if self.performance_evaluations.get(data.tag, None) is not None:
            return
        self.performance_evaluations[data.tag] = data
        self.tags.append(data.tag)
    def get_performance(self, tag):
        return self.performance_evaluations.get(tag, None)
    def get_tags(self):
        return self.tags
    def print_performance(self):
        print('====== Performance Evaluation =======')
        print(self.tags)
        print(self.performance_evaluations)
        for tag in self.tags:
            print(self.performance_evaluations[tag].description)
            print(f'Time taken: {self.performance_evaluations[tag].time} s')
            print()

def performance_check(tag, description):
    def function_handler(f):
        def time_evaluation_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            f(*args, **kwargs)
            end_time = time.perf_counter()
            pI = PerformanceInformation(tag, description, end_time-start_time)
            Performance().add_performance_evaluation(pI)
        return time_evaluation_wrapper
    return function_handler