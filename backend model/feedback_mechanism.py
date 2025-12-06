from typing import Dict

class Feedback:
    def __init__(self, comp_result:Dict):
        self.comp_result = comp_result

    def feedback_result(self) -> str:
        if self.comp_result['dead'] == 4 and self.comp_result['injured'] == 0:
            return 'All dead'

        if self.comp_result['dead'] == 0 and self.comp_result['injured'] == 0:
            return 'No matches'

        else:
            return f'{self.comp_result['dead']}dead and {self.comp_result['injured']}inj'


