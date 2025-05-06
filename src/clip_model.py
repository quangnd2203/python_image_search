import llm
from typing import List, Tuple
from scipy.spatial.distance import cosine


class CLIPModel:
    """
    Wrapper for the CLIP model from the llm library, used to embed images and text,
    compute similarities, and predict the most relevant prompt for an image.
    """

    def __init__(self, model_name: str = "clip"):
        """
        Initialize the embedding model.

        Args:
            model_name (str): Name of the model (default: "clip")
        """
        # Load the CLIP embedding model from the llm library
        self.model = llm.get_embedding_model(model_name)

    def embed_image(self, image_bytes: bytes) -> List[float]:
        """
        Embed an image into a vector representation.

        Args:
            image_bytes (bytes): Raw image data in bytes

        Returns:
            List[float]: Vector representation of the image
        """
        # Embed the image into vector space; batch returns a list so extract the first item
        return self.model.embed_batch([image_bytes])[0]

    def embed_prompts(self, prompts: List[str]) -> List[List[float]]:
        """
        Embed a list of textual prompts into vector space.

        Args:
            prompts (List[str]): Textual prompts

        Returns:
            List[List[float]]: Corresponding list of vector embeddings
        """
        # Convert each text prompt into its vector representation
        return self.model.embed_batch(prompts)

    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute cosine similarity between two vectors.

        Args:
            vec1 (List[float]): First vector
            vec2 (List[float]): Second vector

        Returns:
            float: Similarity score (1.0 is most similar)
        """
        # Cosine similarity: the closer to 1.0, the more similar the vectors
        return 1 - cosine(vec1, vec2)

    def guess_prompt(self, image_vec: List[float], prompts: List[str]) -> Tuple[str, float]:
        """
        Predict which textual prompt best matches a given image.

        Args:
            image_vec (List[float]): Vector embedding of the image
            prompts (List[str]): List of textual prompts to compare

        Returns:
            Tuple[str, float]: Best-matching prompt and its similarity score
        """
        # Embed all prompts into vector space
        prompt_vecs = self.embed_prompts(prompts)

        # Compute similarity scores between the image and each prompt
        scores = [self.similarity(image_vec, pvec) for pvec in prompt_vecs]

        # Pair each prompt with its similarity score
        prompt_score_pairs = zip(prompts, scores)

        # Select the prompt with the highest similarity score
        best_prompt, best_score = max(prompt_score_pairs, key=lambda x: x[1])

        return best_prompt, best_score