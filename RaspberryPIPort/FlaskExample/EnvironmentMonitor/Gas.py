class Gas:
    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp

    def get_value(self):
        return self.value

    def get_timestamp(self):
        return self.timestamp

    def __str__(self):
        # Update string from "Gas Level" to "VOC Index"
        return "VOC Index: " + str(self.value)
