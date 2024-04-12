import sqlite3
from abc import abstractmethod

#this function has nothing to do with OOP, it is for backend too though
def checkIfTableExists():
    conn= sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    print(cursor.fetchall())
    if len(cursor.fetchall())<1:
        try:
            try:
                cursor.execute("""CREATE TABLE tasks(
                        title text,
                        priority text,
                        state text
                    )
                    """)
            except sqlite3.OperationalError():
                pass
            finally:
                pass
        except TypeError:
            pass
        finally: 
            pass
    
    conn.commit()
    conn.close()


# parent class where all other classes are inheriting from
class tasks():
    def __init__(self,title = "",priority = "",oid = 0):
        self.title = title
        self.priority = priority
        self.oid = oid

        checkIfTableExists()

    # declaration of abstract metho, abstract method is a from of declaring a method in a parent class where all child classses can implement the same function in their own way
    @abstractmethod
    def register(self):
        pass
    def mark(self):
        pass
    def remove(self):
        conn= sqlite3.connect('database.db')
        cursor=conn.cursor()
        cursor.execute(f"DELETE FROM tasks WHERE oid={self.oid}")
        conn.commit()
        conn.close()

class highTask(tasks):
    #encapsulation of variable "state"
    state = "no"
    def __init__(self, title = "", priority = "high",oid = 0):
        super().__init__(title, priority)
        self.oid = oid


    #ovverriding of the abstract method register from the parent class
    def register(self):
        self.priority = "high"
        conn= sqlite3.connect('database.db')
        cursor=conn.cursor()
        cursor.execute("INSERT INTO tasks VALUES(:title,:priority,:state)",
            {
                'title': self.title,
                'priority': self.priority,
                'state': self.state
            }
        )
        conn.commit()
        conn.close()
    
    # polymorphism of the mwthod mark from the parent class
    def mark(self):
        conn=sqlite3.connect('database.db')
        cursor=conn.cursor()
        cursor.execute("UPDATE tasks SET state=:new_state WHERE oid=:oid",
            {
                'oid': self.oid,
                'new_state': "done"
            }
        )
        conn.commit()
        conn.close()

# second child class, this class is for the medium level task, it inherits from the parent class "tasks"
class mediumTask(tasks):
    #encapsulation of variable "state"
    state = "no"
    def __init__(self, title = "", priority = "medium",oid = 0):
        super().__init__(title, priority)
        self.oid = oid


    #override abstract method
    def register(self):
        self.priority = "medium"
        conn= sqlite3.connect('database.db')
        cursor=conn.cursor()
        cursor.execute("INSERT INTO tasks VALUES(:title,:priority,:state)",
            {
                'title': self.title,
                'priority': self.priority,
                'state': self.state
            }
        )
        conn.commit()
        conn.close()

    def mark(self):
        conn=sqlite3.connect('database.db')
        cursor=conn.cursor()
        cursor.execute("UPDATE tasks SET state=:new_state WHERE oid=:oid",
            {
                'oid': self.oid,
                'new_state': "done"
            }
        )
        conn.commit()
        conn.close()


class lowTask(tasks):
    #encapsulation of variable "state"
    state = "no"
    def __init__(self, title = "", priority = "low",oid = 0):
        super().__init__(title, priority)
        self.oid = oid


    #override abstract method
    def register(self):
        self.priority = "low"
        conn= sqlite3.connect('database.db')
        cursor=conn.cursor()
        cursor.execute("INSERT INTO tasks VALUES(:title,:priority,:state)",
            {
                'title': self.title,
                'priority': self.priority,
                'state': self.state
            }
        )
        conn.commit()
        conn.close()

    def mark(self):
        conn=sqlite3.connect('database.db')
        cursor=conn.cursor()
        cursor.execute("UPDATE tasks SET state=:new_state WHERE oid=:oid",
            {
                'oid': self.oid,
                'new_state': "done"
            }
        )
        conn.commit()
        conn.close()
