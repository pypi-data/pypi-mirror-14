from __future__ import absolute_import
# Import classes that should be in the Tasks namespace
# Import the list of tasks and the task and abstract job definition
#from TaskList import TaskList

from Ganga.Core.GangaRepository import addRegistry
from .TaskRegistry import TaskRegistry

myTaskRegistry = TaskRegistry("tasks", "Tasks Registry")

addRegistry(myTaskRegistry)

def stopTasks():
    global myTaskRegistry
    myTaskRegistry.stop()

# Tasks
from .Task import Task
from .Transform import Transform

from .ITask import ITask
from .ITransform import ITransform
from .TaskChainInput import TaskChainInput
from .TaskLocalCopy import TaskLocalCopy

from .CoreTask import CoreTask
from .CoreTransform import CoreTransform
from .CoreUnit import CoreUnit

# Start Logger
#import Ganga.Utility.logging
#logger = Ganga.Utility.logging.getLogger()
from .common import logger

from .TaskApplication import ExecutableTask, ArgSplitterTask


