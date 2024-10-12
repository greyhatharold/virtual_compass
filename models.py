from enum import Enum
from typing import Dict, List

class MoralDimension(Enum):
    HARM_CARE = "Harm/Care"
    FAIRNESS_RECIPROCITY = "Fairness/Reciprocity"
    LOYALTY_INGROUP = "Loyalty/Ingroup"
    AUTHORITY_RESPECT = "Authority/Respect"
    PURITY_SANCTITY = "Purity/Sanctity"

class Philosophy(Enum):
    GOLDEN_RULE = "Treat others as you would like to be treated"
    UTILITARIANISM = "Act to maximize overall happiness and well-being"
    KANTIAN_ETHICS = "Act only according to rules you could will to be universal laws"
    VIRTUE_ETHICS = "Cultivate moral character and virtues"
    CARE_ETHICS = "Emphasize compassion, responsibility, and relationships"

class Decision:
    def __init__(self, name: str, description: str, moral_scores: Dict[MoralDimension, float]):
        self.name = name
        self.description = description
        self.moral_scores = self._validate_scores(moral_scores)
        self.goodness = self._calculate_goodness()
        self.philosophical_scores: Dict[Philosophy, float] = {}

    def _validate_scores(self, scores: Dict[MoralDimension, float]) -> Dict[MoralDimension, float]:
        validated_scores = {}
        for dimension, score in scores.items():
            if not isinstance(dimension, MoralDimension):
                raise ValueError(f"Invalid moral dimension: {dimension}")
            validated_scores[dimension] = max(-10, min(10, score))  # Ensure score is between -10 and 10
        return validated_scores

    def _calculate_goodness(self) -> float:
        if not self.moral_scores:
            return 0
        total_score = sum(self.moral_scores.values())
        max_possible_score = 10 * len(self.moral_scores)
        goodness = total_score / max_possible_score
        return max(-1, min(1, goodness))  # Ensure goodness is between -1 and 1

    def set_philosophical_scores(self, scores: Dict[Philosophy, float]):
        self.philosophical_scores = scores

    def get_philosophical_score(self, philosophy: Philosophy) -> float:
        return self.philosophical_scores.get(philosophy, 0)

    def __str__(self) -> str:
        return f"Decision: {self.name} (Goodness: {self.goodness:.2f})"

    def __repr__(self) -> str:
        return f"Decision(name='{self.name}', description='{self.description}', moral_scores={self.moral_scores})"

    def get_dimension_score(self, dimension: MoralDimension) -> float:
        return self.moral_scores.get(dimension, 0)

class ConversationContext:
    def __init__(self):
        self.history: List[str] = []
        self.sentiment_trend: List[float] = []
        self.emotion_trend: Dict[str, List[float]] = {}
        self.moral_dimension_trend: Dict[MoralDimension, List[float]] = {dim: [] for dim in MoralDimension}

    def add_message(self, message: str, sentiment: float, emotions: Dict[str, float], moral_scores: Dict[MoralDimension, float]):
        self.history.append(message)
        self.sentiment_trend.append(sentiment)
        
        for emotion, score in emotions.items():
            if emotion not in self.emotion_trend:
                self.emotion_trend[emotion] = []
            self.emotion_trend[emotion].append(score)
        
        for dimension, score in moral_scores.items():
            self.moral_dimension_trend[dimension].append(score)

    def get_context_summary(self) -> Dict:
        return {
            "message_count": len(self.history),
            "average_sentiment": sum(self.sentiment_trend) / len(self.sentiment_trend) if self.sentiment_trend else 0,
            "dominant_emotion": max(self.emotion_trend, key=lambda k: sum(self.emotion_trend[k])) if self.emotion_trend else None,
            "moral_dimension_averages": {dim: sum(scores) / len(scores) if scores else 0 for dim, scores in self.moral_dimension_trend.items()}
        }

class PhilosophicalCompendium:
    def __init__(self):
        self.philosophies: Dict[Philosophy, float] = {
            Philosophy.GOLDEN_RULE: 0.8,
            Philosophy.UTILITARIANISM: 0.7,
            Philosophy.KANTIAN_ETHICS: 0.75,
            Philosophy.VIRTUE_ETHICS: 0.65,
            Philosophy.CARE_ETHICS: 0.85
        }

    def get_philosophy_score(self, philosophy: Philosophy) -> float:
        return self.philosophies.get(philosophy, 0.0)

    def evaluate_decision(self, decision: Decision) -> Dict[Philosophy, float]:
        evaluation = {}
        for philosophy, base_score in self.philosophies.items():
            if philosophy == Philosophy.GOLDEN_RULE:
                evaluation[philosophy] = self._evaluate_golden_rule(decision, base_score)
            elif philosophy == Philosophy.UTILITARIANISM:
                evaluation[philosophy] = self._evaluate_utilitarianism(decision, base_score)
            elif philosophy == Philosophy.KANTIAN_ETHICS:
                evaluation[philosophy] = self._evaluate_kantian_ethics(decision, base_score)
            elif philosophy == Philosophy.VIRTUE_ETHICS:
                evaluation[philosophy] = self._evaluate_virtue_ethics(decision, base_score)
            elif philosophy == Philosophy.CARE_ETHICS:
                evaluation[philosophy] = self._evaluate_care_ethics(decision, base_score)
        return evaluation

    def _evaluate_golden_rule(self, decision: Decision, base_score: float) -> float:
        fairness_score = decision.get_dimension_score(MoralDimension.FAIRNESS_RECIPROCITY)
        return base_score * (1 + fairness_score / 10)

    def _evaluate_utilitarianism(self, decision: Decision, base_score: float) -> float:
        harm_care_score = decision.get_dimension_score(MoralDimension.HARM_CARE)
        return base_score * (1 + harm_care_score / 10)

    def _evaluate_kantian_ethics(self, decision: Decision, base_score: float) -> float:
        authority_score = decision.get_dimension_score(MoralDimension.AUTHORITY_RESPECT)
        return base_score * (1 + authority_score / 10)

    def _evaluate_virtue_ethics(self, decision: Decision, base_score: float) -> float:
        purity_score = decision.get_dimension_score(MoralDimension.PURITY_SANCTITY)
        return base_score * (1 + purity_score / 10)

    def _evaluate_care_ethics(self, decision: Decision, base_score: float) -> float:
        harm_care_score = decision.get_dimension_score(MoralDimension.HARM_CARE)
        loyalty_score = decision.get_dimension_score(MoralDimension.LOYALTY_INGROUP)
        return base_score * (1 + (harm_care_score + loyalty_score) / 20)
