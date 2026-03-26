# Spaced repetition planner - the actual recommendation algorithm

# Libraries
import sqlite3
import random
from datetime import date

# Modulised so that I can call this from a GUI (hopefully this should be much simpler than)
def spaced_repetition_recommendations(table:str):
    if table.endswith(".db"):
        conn = sqlite3.connect(table)
        date_review = (date.today()).isoformat()
        cursor = conn.execute("SELECT TopicID, TopicDetail FROM Topics WHERE DateToReview <= ?",(date_review,))
        rows = cursor.fetchall()
        chosen_topics = []
        all_subject_topics_editable = rows
        chosen_topics = random.sample(rows, k=min(3, len(rows)))
        conn.close()
        return chosen_topics
        
# # This is mainly for debugging purposes, I will alter it so that it works by clicking a button
# all_subject_topics=spaced_repetition_recommendations("comp_sci_for_me.db")
# chosen_topics = []
# all_subject_topics_editable = all_subject_topics
# chosen_topics = random.sample(all_subject_topics, k=min(3, len(all_subject_topics)))
# print(chosen_topics)

# def test(table:str):
#     conn = sqlite3.connect(table)
#     conn.execute()