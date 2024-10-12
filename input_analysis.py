import spacy
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from models import Decision, MoralDimension, Philosophy, PhilosophicalCompendium
from moral_compass import MoralCompass
from logger import get_logger

class ConversationAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Load emotion classification model and tokenizer
        self.emotion_tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        self.emotion_model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        self.emotion_model.eval()  # Set the model to evaluation mode
        
        self.philosophical_compendium = PhilosophicalCompendium()
        self.logger = get_logger(__name__, log_level="DEBUG")

    def analyze_input(self, text: str) -> dict:
        self.logger.info(f"Analyzing input: {text}")
        
        # Basic NLP analysis
        doc = self.nlp(text)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(text)
        
        # Emotion classification
        emotions = self._classify_emotions(text)
        
        # Extract key phrases and entities
        key_phrases = self._extract_key_phrases(doc)
        entities = self._extract_entities(doc)
        
        # Moral dimension scoring
        moral_scores = self._score_moral_dimensions(doc, sentiment, emotions)
        
        # Create a Decision object
        decision = Decision("User Input", text, moral_scores)
        
        # Generate philosophical evaluation
        philosophical_evaluation = self.philosophical_compendium.evaluate_decision(decision)
        
        analysis_result = {
            "text": text,
            "sentiment": sentiment,
            "emotions": emotions,
            "key_phrases": key_phrases,
            "entities": entities,
            "moral_scores": moral_scores,
            "decision": decision,
            "philosophical_evaluation": philosophical_evaluation,
        }
        
        self.logger.info("Analysis complete")
        return analysis_result

    def _analyze_sentiment(self, text: str) -> dict:
        blob = TextBlob(text)
        vader_sentiment = self.sentiment_analyzer.polarity_scores(text)
        
        return {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity,
            "compound": vader_sentiment["compound"],
            "pos": vader_sentiment["pos"],
            "neu": vader_sentiment["neu"],
            "neg": vader_sentiment["neg"]
        }

    def _classify_emotions(self, text: str) -> dict:
        inputs = self.emotion_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.emotion_model(**inputs)
        
        scores = torch.nn.functional.softmax(outputs.logits, dim=1)
        emotions = {self.emotion_model.config.id2label[i]: score.item() for i, score in enumerate(scores[0])}
        return emotions

    def _extract_key_phrases(self, doc) -> list:
        return [chunk.text for chunk in doc.noun_chunks]

    def _extract_entities(self, doc) -> list:
        return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    def _score_moral_dimensions(self, doc, sentiment: dict, emotions: dict) -> dict:
        moral_scores = {}
        
        # Harm/Care
        harm_care_score = (emotions.get("joy", 0) - emotions.get("sadness", 0) - emotions.get("fear", 0)) * 10
        moral_scores[MoralDimension.HARM_CARE] = max(-10, min(10, harm_care_score))
        
        # Fairness/Reciprocity
        fairness_score = (sentiment["polarity"] + 1) * 5  # Scale from -1:1 to 0:10
        moral_scores[MoralDimension.FAIRNESS_RECIPROCITY] = fairness_score
        
        # Loyalty/Ingroup
        loyalty_score = emotions.get("trust", 0) * 10
        moral_scores[MoralDimension.LOYALTY_INGROUP] = loyalty_score
        
        # Authority/Respect
        authority_score = 5  # Neutral score as it's hard to determine from text alone
        moral_scores[MoralDimension.AUTHORITY_RESPECT] = authority_score
        
        # Purity/Sanctity
        purity_score = (1 - emotions.get("disgust", 0)) * 10
        moral_scores[MoralDimension.PURITY_SANCTITY] = purity_score
        
        return moral_scores

def analyze_conversation(text: str) -> dict:
    analyzer = ConversationAnalyzer()
    return analyzer.analyze_input(text)
