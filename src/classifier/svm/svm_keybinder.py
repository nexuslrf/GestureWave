from pymouse import PyMouse
from pykeyboard import PyKeyboard



class KeyBinder():
    def __init__(self):
        self.m = PyMouse()
        self.k = PyKeyboard()
        self.selectSchema()

    def selectSchema(self, idx=0):
        if idx == 0:
            self.keys_list = [
                [self.k.windows_l_key, self.k.control_key, self.k.right_key],
                [self.k.windows_l_key, 'd'],
                [self.k.windows_l_key, self.k.control_key, self.k.left_key],
                [self.k.windows_l_key, self.k.alt_key],
                [self.k.control_key, '+'],
                [self.k.control_key, '-'] ]
            self.func = ['->', 'desktop', '<-', 'task', 'Zoom +', 'Zoom -']
            print('Windows Control Schema')
        else:
            print('No such schema!')

    def KeyTap(self, num):
        if num != 6:
            self.k.press_keys(self.keys_list[num])
            print('{}: {}'.format(num, self.func[num]))





# k.press_key(k.windows_l_key)
# k.press_key(k.control_key)
# k.tap_key(k.left_key)
# k.release_key(k.windows_l_key)
# k.release_key(k.control_key)