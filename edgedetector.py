# Credit: https://stackoverflow.com/questions/43272049/how-to-execute-a-function-once-when-boolean-value-changes-in-python

class EdgeDetector:
    """Detects False to True transitions on an external signal."""

    def __init__(self):
        self.last_value = False    # initialise value
        self.curr_value = False

    def update_value(self, new_value):
        self.last_value = self.curr_value
        self.curr_value = new_value

    def check_edge(self):
        if self.curr_value and not self.last_value:
            return True
        else:
            return False