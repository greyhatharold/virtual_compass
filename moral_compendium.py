from enum import Enum
from typing import Dict, List
from models import Decision, MoralDimension
import numpy as np

class Philosophy(Enum):
    GOLDEN_RULE = "Treat others as you would like to be treated"
    UTILITARIANISM = "Act to maximize overall happiness and well-being"
    KANTIAN_ETHICS = "Act only according to rules you could will to be universal laws"
    VIRTUE_ETHICS = "Cultivate moral character and virtues"
    CARE_ETHICS = "Emphasize compassion, responsibility, and relationships"

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

class EnhancedMoralCompass:
    def __init__(self, decision: Decision, compendium: PhilosophicalCompendium):
        self.decision = decision
        self.compendium = compendium
        self.philosophical_evaluation = self.compendium.evaluate_decision(self.decision)

    def calculate_compass_direction(self):
        # Use both the decision's goodness and philosophical evaluation
        decision_weight = 0.6
        philosophy_weight = 0.4
        
        decision_goodness = self.decision.goodness
        philosophy_goodness = sum(self.philosophical_evaluation.values()) / len(self.philosophical_evaluation)
        
        combined_goodness = (decision_goodness * decision_weight) + (philosophy_goodness * philosophy_weight)
        
        # Convert goodness to an angle (0 is north, pi is south)
        angle = np.pi * (1 - combined_goodness) / 2
        return angle

    def generate_report(self) -> str:
        report = f"Moral Compass Report for: {self.decision.name}\n"
        report += f"Description: {self.decision.description}\n\n"
        report += f"Overall Goodness: {self.decision.goodness:.2f}\n\n"
        report += "Moral Dimension Scores:\n"
        for dimension, score in self.decision.moral_scores.items():
            report += f"  {dimension.value}: {score:.2f}\n"
        report += "\nPhilosophical Evaluation:\n"
        for philosophy, score in self.philosophical_evaluation.items():
            report += f"  {philosophy.value}: {score:.2f}\n"
        return report

def analyze_decision(decision: Decision, compendium: PhilosophicalCompendium):
    compass = EnhancedMoralCompass(decision, compendium)
    compass.visualize()
    print(compass.generate_report())