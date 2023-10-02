import time


class PerformanceInformation:
    def __init__(self, tag='', description='', timeTaken=0):
        self.time = timeTaken
        self.times = 0
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
            self.performance_evaluations[tag].time += value
            self.performance_evaluations[tag].times += 1
            return
        self.performance_evaluations[parent_tag].subTasks[tag].time += value
        self.performance_evaluations[parent_tag].subTasks[tag].times += 1
    def print_performance(self):
        import config
        if not config.CONFIG['performance-profile']:
            return
        print('====== Performance Evaluation =======')
        for tag in self.tags:
            perfEval = self.performance_evaluations[tag]
            print(perfEval.description)
            print(f'Total Time taken: {perfEval.time} s')
            print(f'Average operation time: {perfEval.time / perfEval.times} s')
            for subTag in perfEval.subTaskTags:
                subTask = perfEval.subTasks[subTag]
                print(f'\t {subTask.description}')
                print(f'\t Total Time taken: {subTask.time} s')
                print(f'\t Average operation time: {subTask.time / subTask.times} s')
            print()

    def make_performance_headers(self, tags):
        headers = ['Entry','Population Size', 'Gene Length', 'Steps Per Generation'] + tags
        return headers
            
    def performance_report(self, tags, headers=False):
        import uuid
        import config
        entry = uuid.uuid4()
        row_data = [entry,config.CONFIG['population-size'], config.CONFIG['gene-length'], config.CONFIG['max-steps']]
        row_data += [self.performance_evaluations[tag].time for tag in tags]
        row_data = list(map(str, row_data))
        with open(f'./{config.CONFIG["image-output-path"]}/reports/performance.csv', 'a') as f:
            if headers:
                f.write(','.join(self.make_performance_headers(tags))+'\n')
            f.write(','.join(row_data)+'\n')

    def subtask_performance_report(self, parent_tag, headers=False):
        import config
        import uuid
        entry = uuid.uuid4()
        row_data = [entry,config.CONFIG['population-size'], config.CONFIG['gene-length'], config.CONFIG['max-steps']]
        row_data += [subTask.time for subTask in self.performance_evaluations[parent_tag].subTasks.values()]
        row_data = list(map(str, row_data)) 
        with open(f'./{config.CONFIG["image-output-path"]}/reports/performance_sub_task.csv', 'a') as f:
            if headers:
                f.write(','.join(self.make_performance_headers(self.performance_evaluations[parent_tag].subTaskTags))+'\n')
            f.write(','.join(row_data)+'\n')

def performance_check(tag, description, parent_tag=''):
    import config
    def function_handler(f):
        def time_evaluation_wrapper(*args, **kwargs):
            if not config.CONFIG['performance-profile']:
                return f(*args, **kwargs)
            pI = PerformanceInformation(tag, description)
            Performance().add_performance_evaluation(pI, parent_tag)
            
            start_time = time.perf_counter()
            returnable = f(*args, **kwargs)
            end_time = time.perf_counter()
            Performance().set_time_value(pI.tag, end_time-start_time, parent_tag)
            return returnable
            
        return time_evaluation_wrapper
    return function_handler