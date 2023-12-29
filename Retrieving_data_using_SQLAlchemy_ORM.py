from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, select
from sqlalchemy.orm import registry, relationship, Session #create objects and classes
password = '123'
engine = create_engine('mysql+mysqlconnector://root:{}@localhost:3306/projects'.format(password), echo=True)

mapper_registry = registry()
# mapper_registry.metadata

base = mapper_registry.generate_base() #begin create models for task tables
class project(base):
    __tablename__ = 'projects' #the name of mysql table
    project_id = Column(Integer, primary_key=True)
    title = Column(String(length=50))
    description = Column(String(length=50))
    def __repr__(self): #printable represantation of the object
        return "<Project(title='{0}, description='{1})".format(self.title, self.description)

class Task(base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    description = Column(String(length=50))

    project = relationship("project")
    def __repr__(self):
        return "<Task(description='{0})>".format(self.description)

base.metadata.create_all(engine)

# Using SQLAlchemy Sessions to transact on a MySQL database
with Session(engine) as session: # session is used for enabling transactions btw databases
    smt = select(project).where(project.title == 'Organize closet') #select the project with the given title
    result = session.execute(smt)
    organize_closet_project = result.scalar() # scalar allows us to select the first row in the result
# chosingg the related tasks 
    smt = select(Task).where(Task.project_id == organize_closet_project.project_id)
    # return all the tasks associated with the project
    result = session.execute(smt)
    for task in result:
        print(task)