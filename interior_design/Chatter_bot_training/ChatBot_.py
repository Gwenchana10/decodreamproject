import nltk
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')  

class ChatBot_:
    def __init__(self):
        self.chatbot = None
    
    def train(self, datafolder="./custom", train_corpus=True):
        self.chatbot = ChatBot(
            'InteriorBot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///database.db',
            logic_adapters=[
                'chatterbot.logic.BestMatch',
                'chatterbot.logic.MathematicalEvaluation'
            ],
            preprocessors=['chatterbot.preprocessors.clean_whitespace'],
            database_adapter='chatterbot.database.SQLDatabaseAdapter',
        )

        trainer = ChatterBotCorpusTrainer(self.chatbot)

        if train_corpus:
            trainer.train('chatterbot.corpus.english')  
        
        if datafolder:
            for filename in os.listdir(datafolder):
                if filename.endswith(".yml"):
                    trainer.train(os.path.join(datafolder, filename))
                    print(f"Training with {filename}")

ChatBot_().train(datafolder="./custom", train_corpus=True)
