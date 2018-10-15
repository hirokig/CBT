import numpy as np
from core.nlp.response_generator.product.base.base_response_generator import BaseResponseGenerator


class AskFinishResponseGenerator(BaseResponseGenerator):
    """
    This class will be accessed when it seems users want to quit the session.
    """

    def __call__(self):
        responses = self.__create_ask_to_finish()
        self.response_data['regular'] = responses

        return self.response_data

    def __create_ask_to_finish(self):
        # TODO ここでnoと答えたuserはsession終わる
        options = [
            ["alright", "let me tell you i am always here for you🤗", "Do you have anything to vent more?"],
            ["I really appreciate that you talk to me a lot today😉",
             "Is there anything you want to tell me more?"],
            ["i see..", "thanks for talking to me so far😊", "anything else you wanna tell me now?"]
        ]

        np.random.shuffle(options)
        return options[0]
