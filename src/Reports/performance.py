import time


class PerformanceInformation:
    def __init__(self, tag='', description='', timeTaken=0):
        self.time = timeTaken
        self.tag = tag
        self.description = description
        self.subTasks = {}
        self.subTaskTags = []
    def add_sub_task(self, performanceInformation):
        if self.subTasks.get(performanceInformation.tag, None) is None:
            self.subTasks[performanceInformation.tag] = performanceInformation
            self.subTaskTags.append(performanceInformation.tag)

class Performance:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Performance, cls).__new__(cls)
        return cls.instance
    
    def config(self):
        self.performance_evaluations = {}
        self.tags = []

    def add_performance_evaluation(self, data, parent_tag):
        if self.performance_evaluations.get(data.tag, None) is not None:
            return
            
        if self.performance_evaluations.get(parent_tag, None) is not None:
            self.performance_evaluations[parent_tag].add_sub_task(data)
        else:
            self.performance_evaluations[data.tag] = data
            self.tags.append(data.tag)

    def set_time_value(self, tag, value, parent_tag=''):
        if parent_tag == '':
            self.performance_evaluations[tag].time = value
            return
        self.performance_evaluations[parent_tag].subTasks[tag].time = value
    def print_performance(self):
        print('====== Performance Evaluation =======')
        for tag in self.tags:
            perfEval = self.performance_evaluations[tag]
            print(perfEval.description)
            print(f'Time taken: {perfEval.time} s')
            for subTag in perfEval.subTaskTags:
                subTask = perfEval.subTasks[subTag]
                print(f'\t {subTask.description}')
                print(f'\t Time taken: {subTask.time} s')
            print()

def performance_check(tag, description, parent_tag=''):
    def function_handler(f):
        def time_evaluation_wrapper(*args, **kwargs):
            pI = PerformanceInformation(tag, description)
            Performance().add_performance_evaluation(pI, parent_tag)
            
            start_time = time.perf_counter()
            returnable = f(*args, **kwargs)
            end_time = time.perf_counter()
            Performance().set_time_value(pI.tag, end_time-start_time, parent_tag)
            return returnable
            
        return time_evaluation_wrapper
    return function_handler