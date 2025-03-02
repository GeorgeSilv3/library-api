class Book:
    def __init__(self, id, name, author, edition):
         self.__id = id
         self.__name = name
         self.__author = author
         self.__edition = edition

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name
    
    def get_author(self):
        return self.__author
    
    def get_edition(self):
        return self.__edition
    
    def set_name(self, name):
        self.__name = name
    
    def set_author(self, author):
        self.__author = author
    
    def set_edition(self, edition):
        self.__edition = edition

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "author": self.__author,
            "edition": self.__edition
        }