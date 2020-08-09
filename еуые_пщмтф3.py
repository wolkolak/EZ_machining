class Singleton:
    __instance = None
    def __init__(self):
        if not Singleton.__instance:
            print(" __init__ method called..")
            #self.her = 0
        else:
            print("Instance already created:", self.getInstance())
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Singleton()
        return cls.__instance
s = Singleton() ## class initialized, but object not created
print(s)
print("Object created", Singleton.getInstance()) # Object gets created here
print(s)
s = Singleton() ## instance already created


print(s)