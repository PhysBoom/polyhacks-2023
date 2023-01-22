from sentence_transformers import SentenceTransformer, util

class SentenceAnalyzer:

    """
    A singleton class for sentence analysis.
    """
    __instance = None

    def __init__(self):
        if SentenceAnalyzer.__instance is not None:
            raise Exception("SentenceAnalyzer is a singleton class!")
        SentenceAnalyzer.__instance = self
        self.model = SentenceTransformer("distiluse-base-multilingual-cased-v2")

    @staticmethod
    def get_instance():
        if SentenceAnalyzer.__instance is None:
            SentenceAnalyzer()
        return SentenceAnalyzer.__instance

    def get_similarity_scores(self, s1, s2):
        embedding1 = self.model.encode(s1, convert_to_tensor=True)
        embedding2 = self.model.encode(s2, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
        return cosine_scores.item()