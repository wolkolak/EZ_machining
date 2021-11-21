
from abc import ABC
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
from Settings.settings import default_processor, default_machine
import importlib


class DefaultReference(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_default_machine()
        self.get_default_processor()


    def get_default_processor(self):
        self.default_processor_adress = default_processor
        #todo это не обязательно по дефолту


    def get_default_machine(self):
        str1 = default_machine.replace('/', '.') + '.REAL_MACHINE' # path +
        module_real = importlib.import_module(str1)
        self.default_machine = module_real.REAL_MACHINE(None)

