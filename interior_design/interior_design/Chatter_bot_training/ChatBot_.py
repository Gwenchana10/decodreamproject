import nltk
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

class ChatBotTrainer:
    def __init__(self, name='InteriorBot', db_uri='sqlite:///database.db'):
        self.chatbot = ChatBot(
            name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=db_uri,
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I am sorry, I do not understand. Can you rephrase?',
                    'maximum_similarity_threshold': 0.90
                },
                'chatterbot.logic.MathematicalEvaluation'
            ],
            preprocessors=['chatterbot.preprocessors.clean_whitespace']
        )
        self.trainer_corpus = ChatterBotCorpusTrainer(self.chatbot)
        self.trainer_list = ListTrainer(self.chatbot)

    def train_from_corpus(self):
        print("Training with ChatterBot English corpus...")
        self.trainer_corpus.train('chatterbot.corpus.english.greetings')
        print("✓ English corpus training completed.")

    def train_from_custom_folder(self, folder_path="./custom"):
        print(f"Training from custom folder: {folder_path}")
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if file.endswith(".yml"):
                print(f"→ Training with {file}")
                self.trainer_corpus.train(file_path)
        print("✓ Custom YAML corpus training completed.")

    def train_from_conversations(self):
        common_conversations = [
            ["Hello", "Hi there!"],
            ["Hi", "Hello!"],
            ["Hey", "Hey! How can I help you?"],
            ["How are you?", "I'm doing well, how about you?"],
            ["How do you feel?", "I'm an AI, but I'm here to assist you!"],
            ["What is your name?", "I am InteriorBot, your assistant!"],
            ["Can you tell me a joke?", "Why don't scientists trust atoms? Because they make up everything!"],
            ["Tell me something funny", "Why did the chicken cross the road? To get to the other side!"],
            ["Who created you?", "I was created by a developer using ChatterBot!"],
            ["What can you do?", "I can help answer your questions, tell jokes, and chat with you!"],
            ["Thank you", "You're welcome!"],
            ["Bye", "Goodbye! Have a great day!"]
        ]

    # Flatten the list of conversations
        flattened_conversations = [item for sublist in common_conversations for item in sublist]

        print("Training with common small talk conversations...")
        self.trainer_list.train(flattened_conversations)
        print("✓ Small talk training completed.")

    def full_train(self, datafolder="./custom", train_corpus=True):
        if train_corpus:
            self.train_from_corpus()

        if datafolder and os.path.exists(datafolder):
            self.train_from_custom_folder(datafolder)

        self.train_from_conversations()

        print("🎉 All training completed successfully!")

# Example Usage:
if __name__ == "__main__":
    bot_trainer = ChatBotTrainer()
    bot_trainer.full_train(datafolder="./custom", train_corpus=True)
