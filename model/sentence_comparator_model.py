from sentence_transformers import SentenceTransformer, util


class SentenceComparator:
    def __init__(self, sentence_transformer: SentenceTransformer):
        self._sentence_transformer: SentenceTransformer = sentence_transformer
        
    def get_similarity(self, sentence_1: str, sentence_2: str) -> float:
        cosine_scores = util.pytorch_cos_sim(
            self._sentence_transformer.encode(sentence_1, convert_to_tensor=True),
            self._sentence_transformer.encode(sentence_2, convert_to_tensor=True)
        )
        
        return cosine_scores[0][0].item()
    