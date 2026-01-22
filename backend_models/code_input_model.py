

class CodeInputViewModel:
    def __init__(self,
                 screen_type: str,
                 label: str ='BaseCodeLabel',
                 command_on_click= None
                 ):

        self.screen_type = screen_type
        self.label = label
        self.command_on_click = command_on_click
