from typing import Dict

class Feedback:
    def __init__(self, feedback_data:Dict):
        self.feedback_data = feedback_data

    def feedback_result(self) -> str:
        if self.feedback_data['dead'] == 4 and self.feedback_data['injured'] == 0:
            return 'All dead'

        if self.feedback_data['dead'] == 0 and self.feedback_data['injured'] == 0:
            return 'No matches'

        else:
            return f'{self.feedback_data['dead']}dead and {self.feedback_data['injured']}inj'

    def structure_feedback_msg(self, feedback_msg: str, current_guess: list[int]) -> str:
        structured_data = f'{''.join(str(d) for d in current_guess)}  -  {feedback_msg}'
        return structured_data



