#encoding=utf-8
from chatter_learning.brains import ClosestMean
from chatter_learning.store_adapters import Mongodb


class Chatter(object):
    def __init__(self, **kwargs):
        brain_name = kwargs.get('brain', 'closest_mean')
        storage_name = kwargs.get('brain', 'mongodb')
        self.set_store(storage_name, **kwargs)
        self.set_brain(brain_name, **kwargs)
        self.connected_brain_on_store()
        self.recent_conversations = []
    def set_store(self, store_adapter_name, **kwargs):
        if store_adapter_name == 'mongodb':
            self.store = Mongodb(**kwargs)

    def set_brain(self, brain_name, **kwargs):
        if brain_name == 'closest_mean':
            self.brain = ClosestMean(**kwargs)

    def connected_brain_on_store(self):
        self.brain.set_store(self.store)

    def get_previous_conversation(self):
        return self.recent_conversations[-1]

    def append_answer_to_conversation(self, conversation, answer):
        if conversation['answers'] is None:
            conversation['answers'] = []
        conversation['answers'].append(answer)

    def response_to(self, ask):
        confidence, response = self.brain.process(ask)
        current_conversation = {
            'ask': ask,
            'answers': []
        }
        conversation = self.store.get(ask)
        if conversation:
            current_conversation = conversation
        if len(self.recent_conversations) > 0:
            previous_conversation = self.get_previous_conversation()
            self.store.put_answer(previous_conversation['ask'], ask)
        self.recent_conversations.append(current_conversation)
        return response

