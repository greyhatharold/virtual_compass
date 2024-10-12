import random
from models import Decision, Philosophy, PhilosophicalCompendium, MoralDimension
from logger import get_logger
from input_analysis import ConversationAnalyzer

class ResponseGenerator:
    def __init__(self):
        self.compendium = PhilosophicalCompendium()
        self.shakespearean_words = [
            "forsooth", "verily", "prithee", "anon", "methinks", "perchance",
            "hark", "alas", "wherefore", "thusly", "mayhap", "beseech"
        ]
        self.ethical_adjectives = [
            "virtuous", "noble", "righteous", "just", "honorable", "upright",
            "moral", "ethical", "principled", "scrupulous", "conscientious"
        ]
        self.logger = get_logger(__name__, log_level="DEBUG")
        self.conversation_analyzer = ConversationAnalyzer()

    def generate_response(self, text: str) -> str:
        self.logger.debug("Generating response for input", text=text)
        
        analysis_result = self.conversation_analyzer.analyze_input(text)
        
        decision = analysis_result['decision']
        philosophical_scores = self.compendium.evaluate_decision(decision)
        decision.set_philosophical_scores(philosophical_scores)

        shakespearean_response = self._generate_shakespearean_response(decision, analysis_result)
        ethical_analysis = self._generate_ethical_analysis(decision, analysis_result)
        
        combined_response = self._combine_responses(shakespearean_response, ethical_analysis)
        self.logger.debug("Response generated", response=combined_response)
        return combined_response

    def _generate_shakespearean_response(self, decision: Decision, analysis_result: dict) -> str:
        sentiment = analysis_result['sentiment']
        emotions = analysis_result['emotions']
        moral_scores = analysis_result['moral_scores']

        if decision.goodness > 0.6:
            verdict = "most virtuous and commendable"
        elif decision.goodness > 0.2:
            verdict = "generally sound, though not without its perils"
        elif decision.goodness > -0.2:
            verdict = "a matter of great complexity, with virtue and vice intertwined"
        elif decision.goodness > -0.6:
            verdict = "fraught with moral hazard, requiring utmost caution"
        else:
            verdict = "most troubling, and mayhap best avoided"

        dominant_emotion = max(emotions, key=emotions.get)
        dominant_moral_dimension = max(moral_scores, key=moral_scores.get)

        response = f"Hark! {self._random_word()} The matter of '{decision.name}' appears {verdict}. " \
                   f"'Tis a decision most {self._random_adjective()}, worthy of our deepest contemplation. " \
                   f"The sentiment doth lean {self._sentiment_to_shakespearean(sentiment['compound'])}, " \
                   f"with emotions of {dominant_emotion} prevailing. " \
                   f"In the realm of morality, the dimension of {dominant_moral_dimension.value} stands foremost. " \
                   f"{self._random_word().capitalize()} let us ponder it well, for in our choices lie the seeds of our character."
        
        return response

    def _generate_ethical_analysis(self, decision: Decision, analysis_result: dict) -> str:
        dominant_emotion = max(analysis_result['emotions'], key=analysis_result['emotions'].get)
        dominant_moral_dimension = max(analysis_result['moral_scores'], key=analysis_result['moral_scores'].get)
        
        analysis = f"Ethical Analysis of '{decision.name}':\n\n"
        
        # Overall Moral Standing
        analysis += "1. Overall Moral Standing:\n"
        analysis += f"The decision's goodness score is {decision.goodness:.2f}, which "
        if decision.goodness > 0.5:
            analysis += "suggests it leans towards being ethically sound. However, we must carefully consider its implications.\n"
        elif decision.goodness > 0:
            analysis += "indicates some positive ethical aspects, but there's significant room for improvement.\n"
        elif decision.goodness > -0.5:
            analysis += "raises serious ethical concerns and requires careful reconsideration.\n"
        else:
            analysis += "indicates severe ethical issues that strongly suggest against this course of action.\n"
        
        # Emotional Context
        analysis += "\n2. Emotional Context:\n"
        analysis += f"The prevailing emotion of {dominant_emotion} "
        if dominant_emotion in ['joy', 'trust']:
            analysis += "might indicate a positive disposition, but we must be cautious of overlooking potential ethical pitfalls due to optimism.\n"
        elif dominant_emotion in ['anger', 'disgust', 'fear']:
            analysis += "suggests underlying issues that need to be addressed. This emotional response could be indicative of ethical red flags.\n"
        else:
            analysis += "requires further exploration to understand its impact on the ethical implications of this decision.\n"
        
        # Moral Framework
        analysis += f"\n3. Moral Framework:\n"
        analysis += f"The primary moral consideration is {dominant_moral_dimension.value}. "
        if dominant_moral_dimension == MoralDimension.HARM_CARE:
            analysis += "We must carefully evaluate the potential harm or benefit this decision may cause to all parties involved.\n"
        elif dominant_moral_dimension == MoralDimension.FAIRNESS_RECIPROCITY:
            analysis += "It's crucial to ensure that this decision promotes fairness and doesn't unfairly advantage or disadvantage any group.\n"
        elif dominant_moral_dimension == MoralDimension.LOYALTY_INGROUP:
            analysis += "While loyalty is important, we must be cautious of in-group favoritism that might lead to unethical treatment of others.\n"
        elif dominant_moral_dimension == MoralDimension.AUTHORITY_RESPECT:
            analysis += "Respect for authority should be balanced with critical thinking and ethical considerations.\n"
        elif dominant_moral_dimension == MoralDimension.PURITY_SANCTITY:
            analysis += "We should consider how this decision aligns with broader ethical principles and societal values.\n"
        
        # Philosophical Perspectives
        analysis += "\n4. Philosophical Perspectives:\n"
        for philosophy, score in decision.philosophical_scores.items():
            analysis += f"- {philosophy.value}: {score:.2f}\n"
        top_philosophy = max(decision.philosophical_scores, key=decision.philosophical_scores.get)
        analysis += f"\nFrom the perspective of {top_philosophy.value}, "
        if top_philosophy == Philosophy.GOLDEN_RULE:
            analysis += "we should consider how we would feel if we were on the receiving end of this decision.\n"
        elif top_philosophy == Philosophy.UTILITARIANISM:
            analysis += "we must evaluate whether this decision truly maximizes overall well-being for all affected parties.\n"
        elif top_philosophy == Philosophy.KANTIAN_ETHICS:
            analysis += "we should reflect on whether we would will the principle behind this decision to become a universal law.\n"
        elif top_philosophy == Philosophy.VIRTUE_ETHICS:
            analysis += "we should consider how this decision reflects on our character and whether it aligns with virtuous traits.\n"
        elif top_philosophy == Philosophy.CARE_ETHICS:
            analysis += "we must carefully consider the impact on relationships and our responsibilities to others.\n"
        
        # Recommendation
        analysis += "\n5. Recommendation:\n"
        if decision.goodness > 0.3:
            analysis += "While the decision has some positive aspects, it's crucial to address the ethical concerns raised above before proceeding. Consider ways to mitigate potential negative impacts and enhance the positive outcomes."
        elif decision.goodness > -0.3:
            analysis += "Given the significant ethical concerns, it's strongly advised to reconsider this decision. Explore alternative options that better align with ethical principles and address the issues raised in this analysis."
        else:
            analysis += "The ethical analysis strongly suggests against this course of action. It's highly recommended to abandon this decision and seek alternatives that are more ethically sound and aligned with moral principles."
        
        return analysis

    def _combine_responses(self, shakespearean_response: str, ethical_analysis: str) -> str:
        combined = f"{shakespearean_response}\n\nUpon further reflection:\n{ethical_analysis}"
        return combined

    def _random_word(self) -> str:
        return random.choice(self.shakespearean_words)

    def _random_adjective(self) -> str:
        return random.choice(self.ethical_adjectives)

    def _sentiment_to_shakespearean(self, sentiment_score: float) -> str:
        if sentiment_score > 0.5:
            return "most favorably"
        elif sentiment_score > 0:
            return "with a gentle warmth"
        elif sentiment_score > -0.5:
            return "with a touch of melancholy"
        else:
            return "towards the shadows of discontent"
