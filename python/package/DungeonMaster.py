from package import GPTModel, SummarizedConversation
from prompts import PROMPTS

class SummarizedConversation:

    def __init__(self):
        self.model_summarize = GPTModel.GPTModel()
        self.conversation = SummarizedConversation.SummerizedConversation(self.model_summarize,
                                                                          recent_max_chars = 500, 
                                                                          current_max_chars = 500,
                                                                          ancient_max_chars = 4000,
                                                                          max_chars = 4000)
        self.terminate = False
        self.model_dm = GPTModel.GPTModel(system_prompt=PROMPTS['dm_base'])
        self.encyclopedia = {}
        self.model_encyclopedia = GPTModel.GPTModel()
        self.model_controller = GPTModel.GPTModel()
        self.experts = [
            {
                'name': 'combat',
                'version': 'gpt-4',
                'model': None,
                'memory': None,
                'systemPrompt': PROMPTS['combat_system'],
                'initialPrompt': PROMPTS['combat_initial'],
                'criticPrompt': PROMPTS['combat_critic']
            },
            {
                'name': 'adventure',
                'version': 'gpt-3.5-turbo',
                'model': None,
                'memory': None,
                'systemPrompt': PROMPTS['combat_system'],
                'initialPrompt': PROMPTS['adventure_initial'],
                'criticPrompt': PROMPTS['adventure_critic']
            },
            {
                'name': 'character',
                'version': 'gpt-4',
                'model': None,
                'memory': None,
                'systemPrompt': PROMPTS['combat_system'],
                'initialPrompt': PROMPTS['character_initial'],
                'criticPrompt': PROMPTS['character_critic']
            }
        ]
        self.max_drafts = 6

    def user_reply(self, message):
        self.conversation.add_message("User", message)

    def dm_reply(self, message):
        self.conversation.add_message("DM", message)

    def console_reply(self, message):
        self.conversation.add_message("Console", message)

    def initialize(self):

        for expert in self.experts:
            expert.model = GPTModel(model=expert.version, system_prompt=expert.systemPrompt)
            expert.memory = SummarizedConversation(GPTModel.GPTModel(), max_chars=2000, recent_max_chars = 400, 
                 ancient_max_chars = 1000, current_max_chars = 400)

    def get_context(self):
        context = "Here is a summary of the whole adventure so far: \n"
        context += self.conversation.ancient + "\n"
        context += "Here is a summary of only more recent events: \n"
        context += self.conversation.recent + "\n"
        context += "Here is a summary of the currently unfolding events: \n"
        context += self.conversation.current + "\n"
        context += "Finally, here are the most recent exchanges between the DM and the user: \n"
        context += self.conversation.dump(-6)

        return context
    
    def get_experts_initial(context):
        return "No tips needed."
    
    def get_experts_criticism(context, draft):
        return "No feedback needed."
    
    def play(self, message):
        self.user_reply(message)

        self.model_dm.reset()
        context = self.get_context()

        initial_prompt = context + PROMPTS['dm_initial'] + self.get_experts_initial(context)
        draft = self.model_dm.generate_assistant_reply(initial_prompt)

        draft_num = 1
        finished = False
        while draft_num < self.max_drafts and not finished:
            criticism = self.get_experts_criticism(context, draft)

            controller_decision = self.model_controller.generate_assistant_reply(draft, criticism)
            
            self.model_dm.generate_assistant_reply(criticism)

            draft_num += 1