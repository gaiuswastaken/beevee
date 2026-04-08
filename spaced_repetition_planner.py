# Spaced repetition planner - the actual recommendation algorithm

# Libraries
import os
import sqlite3
import random
from datetime import date, timedelta

# Modulised so that I can call this from a GUI (hopefully this should be much simpler)
def spaced_repetition_recommendations(table:str):
    ABS_PATH = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(ABS_PATH, table)
    if table.endswith(".db"):
        conn = sqlite3.connect(db_path)
        # Ensures tasks can be recommended in advance (useful if user just started using the app and has no tasks that are due for review today, this way they can still get recommendations for what to review)
        date_review = (date.today() + timedelta(days=1)).isoformat()
        cursor = conn.execute("SELECT TopicID, TopicDetail FROM Topics WHERE DateToReview <= ?",(date_review,))
        rows = cursor.fetchall()
        chosen_topics = []
        chosen_topics = random.sample(rows, k=min(3, len(rows)))
        conn.close()
        return chosen_topics
