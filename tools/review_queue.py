"""
Interactive review queue.

Allows generated files to be reviewed before being written or committed.
"""

from dataclasses import dataclass

@dataclass
class ReviewItem:
    path:str
    action:str
    approved:bool=False

class ReviewQueue:
    def __init__(self):
        self.items=[]

    def add(self,path,action):
        self.items.append(ReviewItem(path,action))

    def summary(self):
        return [{"path":i.path,"action":i.action,"approved":i.approved} for i in self.items]
