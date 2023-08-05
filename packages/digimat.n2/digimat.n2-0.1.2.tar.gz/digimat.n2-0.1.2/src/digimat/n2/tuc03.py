from n2open import N2OpenDevice

class TUC03(N2OpenDevice):
    def onInit(self):
        self.alias(self.InternalFloat(12), 'ambiance')
        self.alias(self.InternalByte(111), 't2enable')

    def onPing(self):
        if self['ambiance'].readCurrentValue() is not None:
            return True

    def ambiance(self):
        return self.item('ambiance').readCurrentValue()

    def t2enable():
        item=self.item('t2enable')
        def fget(self):
            return item.readCurrentValue()
        def fset(self, value):
            return item.write(value)
        return locals()




