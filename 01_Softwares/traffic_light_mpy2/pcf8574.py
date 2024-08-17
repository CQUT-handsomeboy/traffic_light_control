class PCF8574:
    def __init__(self, i2c, write_address=0b00100111, read_address=0b10100111):
        self.i2c = i2c
        self.write_address = write_address
        self.read_address = read_address

    def output(self, pins_states: int):
        """
        写入一个0x00到0xFF的整数，一次性控制所有的IO口
        """
        assert 0 <= pins_states <= 255
        self.i2c.writeto(self.write_address, bytes((pins_states,)))

    def input(self):
        """
        读入一个0x00到0xFF的整数，一次性读取所有的IO口
        """
        pins_states = self.i2c.readfrom(self.read_address, 1)
        return pins_states