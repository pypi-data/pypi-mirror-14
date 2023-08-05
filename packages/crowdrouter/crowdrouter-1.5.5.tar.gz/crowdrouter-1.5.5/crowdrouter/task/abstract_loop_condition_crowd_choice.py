from abc import ABCMeta, abstractmethod
from ..decorators import choice

class AbstractLoopConditionCrowdChoice(AbstractCrowdChoice):
    t1 = None
    workflow = None

    def __init__(self, crowd_request):
        self.t1 = crowd_request.task
        self.workflow = crowd_request.workflow

    #Use this implementation to provide the looping condition.
    def execute(self, crowd_request, **kwargs):
        task = self.choice(crowd_request)(self.workflow)
        if task == None:
            return None
        return task.execute(crowd_request)

    def get_name(self):
        return self.__class__.__name__

    @choice
    def choice(self, crowd_request):
        pass
