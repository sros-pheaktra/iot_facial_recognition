import numpy as np


class FaceEmbedding:

    def generate(self, face):
        """
        Generate embedding from InsightFace detected face.
        """

        if face.embedding is None:
            return None

        embedding = face.embedding

        return embedding


    def normalize(self, embedding):
        """
        Normalize embedding for comparison.
        """

        norm = np.linalg.norm(embedding)

        if norm == 0:
            return embedding

        return embedding / norm


    def compare(self, embedding1, embedding2):
        """
        Compare two face embeddings using cosine similarity.
        """

        embedding1 = self.normalize(embedding1)
        embedding2 = self.normalize(embedding2)


        similarity = np.dot(
            embedding1,
            embedding2
        )


        return similarity