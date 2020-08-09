from abc import ABCMeta, abstractmethod

class Animal(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, species, body_size, character):
        self.species = species
        self.body_size = body_size
        self.character = character
        if self.species == '食肉' and (self.body_size == '中' or self.body_size == '大') and self.character == '凶猛':
            self.is_fierce = '是'
        else:
            self.is_fierce = '不是'

class Cat(Animal):
    sound = '喵喵'
    def __init__(self,name, species, body_size, character, pet = '适合'):
        super(Cat, self).__init__(species, body_size, character)
        self.name = name
        self.pet = pet

class Zoo(object):
    def __init__(self, name):
        self.name = name
        self.animal = []
        self.animal_type = set()

    @property
    def Cat(self):
        if 'Cat' in self.animal_type:
            return '有'
        else:
            return '没有'

    def add_animal(self, ani):
        name = ani.name
        if name in self.animal:
            print('{} 已经在动物园里了，请不要重复添加!'.format(name))
            return
        self.animal.append(ani.name)
        self.animal_type.add(ani.__class__.__name__)
    

if __name__ == '__main__':
    c = Cat('大脸猫', '食肉', '小', '温顺')
    c2 = Cat('大猫','食肉', '大','凶猛')
    print(c.name, c.species, c.body_size, c.character, c.is_fierce, c.sound, c.pet)
    z = Zoo('时间动物园')
    z.add_animal(c)
    z.add_animal(c)
    z.add_animal(c2)
    print(getattr(z,'Cat'))  
    print(c2.name, c2.species, c2.body_size, c2.character, c2.is_fierce, c2.sound, c2.pet)
    print(z.animal)
    b = Animal('食肉', '小', '温顺')
    



