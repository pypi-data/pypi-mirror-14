pyundo
======

A task flow in Python with ``do`` and ``undo``.

Example
=======

::

  from __future__ import print_function
  from pyundo import TaskBase, LineFlow


  class Task(TaskBase):
      def __init__(name):
          self.name = name

      def do(self):
          print("Do the task: {0}".format(self.name))

      def undo(self):
          print("Undo the task: {0}".format(self.name))


  def main():
      flow = LineFlow()
      flow.add(Task("task1"))
      flow.add(Task("task2"))
      flow.add(Task("task3"))
      flow.execute()


  if __name__ == "__main__":
      main()
