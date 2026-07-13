import numpy as np


class FaceRecognition:
    def __init__(self, database):
        self.database = database
    def cosine_similarity(
        self,
        embedding1,
        embedding2
    ):

        embedding1 = embedding1 / np.linalg.norm(
            embedding1
        )

        embedding2 = embedding2 / np.linalg.norm(
            embedding2
        )
        return np.dot(
            embedding1,
            embedding2
        )
    def recognize(self, embedding):
        users = self.database.get_all_users()
        best_match = None
        highest_score = 0
        for user in users:
            stored_embedding = (
                self.database
                .bytes_to_embedding(
                    user[6]
                )
            )
            score = self.cosine_similarity(
                embedding,
                stored_embedding
            )
            if score > highest_score:
                highest_score = score
                best_match = user
        # Threshold
        if highest_score > 0.6:
            return {
                "name": best_match[1],
                "student_id": best_match[2],
                "major": best_match[3],
                "role": best_match[4],
                "score": highest_score
            }
        return None