import sqlite3
from datetime import date, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from math import ceil, exp

# The weights used in FSRS-4.5 (FSRS 5 and 6 are redundant for me as they account same day review which is not necessary for my algo)
w = [
    0.4872, 1.4003, 3.7145, 13.8206,
    5.1618, 1.2298, 0.8975, 0.031,
    1.6474, 0.1367, 1.0461,
    2.1072, 0.0793, 0.3246, 1.587,
    0.2272, 2.8755
]

# Functions I can use to calculate the time after the retrievability drops below 90% 

def calculate_retrievability(time:float, stability: float):
    # Constants that help clean up the formula
    FACTOR = 19/81
    DECAY = -0.5
    retrievability = (1 + FACTOR * (time/stability)) ** DECAY
    return retrievability

# similar to calculate_retrievability but this time it calculates the time delta before the retrievability drops below 90%
def calculate_next_interval(stability: float, target_retention: float = 0.80):
    FACTOR = 19/81
    DECAY = -0.5
    next_interval = (stability/FACTOR) * (target_retention ** (1/DECAY) - 1)
    next_interval = ceil(next_interval) # Finds the ceiling of next_interval, making the time delta an integer
    return next_interval

def update_stability_success(stability:float, difficulty: float, retrievability: float, grade:float):
    w8 = w[8]
    w9 = w[9]
    w10 = w[10]
    if grade == 2:
        rating_modifier = w[15]
    elif grade == 4:
        rating_modifier = w[16]
    else:
        rating_modifier = 1.0    
    
    gain = exp(w8) * (11 - difficulty) * (stability ** (-w9)) * (exp(w10 * (1-retrievability)) - 1) * rating_modifier
    stability_new = stability * (1+gain) 
    return stability_new

def update_stability_fail(stability: float, difficulty: float, retrievability: float):
    w11 = w[11]
    w12 = w[12]
    w13 = w[13]
    w14 = w[14]
    
    stability_new = w11 * (difficulty ** (-w12)) * ((stability + 1) ** w13 - 1) * exp(w14 * (1 - retrievability))
    return stability_new

def update_difficulty(difficulty: float, grade:int):
    w4 = w[4]
    w5 = w[5]
    w6 = w[6]
    w7 = w[7]
    
    base = (w4 - (grade - 3) * w5 + 1)
    difficulty_new = w7 * base + (1 - w7) * difficulty
    return difficulty_new

# If difficulty and stability are blank, then this function is called

def init_fsrs_ratings(grade: int):
    stability = w[grade - 1] # Inital stability
    
    w4 = w[4]
    w5 = w[5]
    difficulty = w4 - (grade - 3) * w5
    
    return stability, difficulty

def _get_conn(db_path: str) -> sqlite3.Connection:
    if not db_path:
        raise ValueError("db_path must be provided")
    p = Path(db_path)
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    return conn


def get_topics(db_path: str, limit: int = 350) -> List[Dict]:
    # Fetches the list of rows as dictionaries. This allows for faster reading and writing. Difficulty and Stability will be omitted from the user as they do not need to know that however it is useful for calculation
    with _get_conn(db_path) as conn:
        cur = conn.execute(
            "SELECT TopicID, MainCategory, SubCategory, TopicDetail, Grade, Difficulty, Stability,  DateReviewed, DateToReview FROM topics LIMIT ?",
            (limit,),
        )
        return [dict(r) for r in cur.fetchall()]


def update_grade(db_path: str, topic_id: int, grade: int):
    # Sets a Grade between 1-4 for `TopicID`, update `DateReviewed` to today and `DateToReview` to today + delta (calculated via FSRS algo).
    # Rules: Calculated by FSRS algorithm. Dates stored as YYYY-MM-DD strings.
    
    if topic_id is None:
        raise ValueError("topic_id must be provided")

    if grade not in (1,2,3,4):
        raise ValueError("Grade must be between 1-4, 1 being the hardest and 4 being the easiest")

    today = date.today()
    # Fetches the current difficulty and stability with SQL
    with _get_conn(db_path) as conn:
        cursor = conn.execute("SELECT Difficulty, Stability FROM Topics where TopicID = ?",(topic_id,)) # The SQL Query
        calculation_data = cursor.fetchone() # Converts the query into a Row Object
    if calculation_data == None:
        raise ValueError(f"No topic with topic id: {topic_id}")
    
    # I am expecting this to get values of the difficulty and stability
    difficulty = calculation_data["Difficulty"] # Converts into float
    stability = calculation_data["Stability"] # Converts into float
        
    
    # If this is a new topic that just got updated
    if difficulty == None or stability == None:
        listy = init_fsrs_ratings(grade)
        stability = listy[0]
        difficulty = listy[1]
    
    # To calculate retrievability, I fetch the value of DateReviewed and feed it into calculate_retrievability()
    
    with _get_conn(db_path) as conn:
        cursor = conn.execute("SELECT DateReviewed FROM Topics where TopicID = ?",(topic_id,)) # The SQL Query
        date_object = cursor.fetchone() # Converts the query into a Row Object
    if date_object == None:
        raise ValueError(f"No topic with topic id: {topic_id}")
    
    
    date_last_reviewed = date_object["DateReviewed"]
    # Prevents a bug where I cannot update the DateReviewed if it is None (1st review)
    if date_last_reviewed == None:
        date_last_reviewed = today
    else:
        date_last_reviewed = date.fromisoformat(date_last_reviewed)
    # I need to clarify, the date_just_reviewed variable is the date when you are planning to update the grade    
    date_just_reviewed = today
    elapsed_days =(date_just_reviewed-date_last_reviewed).days
    calculated_retrievability = calculate_retrievability(elapsed_days, stability)
        
    difficulty_new = update_difficulty(difficulty, grade)
    
    # There are two ways to update stability, if grade is 1 or if it is between 2 and 4
    if grade == 1:
        stability_new = update_stability_fail(stability, difficulty, calculated_retrievability)
    elif grade in (2,3,4): # Expected grades 2,3,4
        stability_new = update_stability_success(stability, difficulty, calculated_retrievability, grade)
    else:
        raise ValueError("Grade must be between 1-4, 1 being the hardest and 4 being the easiest")    
    
    delta_days = calculate_next_interval(stability_new)

    date_to_review = (today + timedelta(days=delta_days)).isoformat()

    with _get_conn(db_path) as conn:
        conn.execute(
            "UPDATE topics SET Grade = ?, Difficulty = ?, Stability = ?,  DateReviewed = ?, DateToReview = ? WHERE TopicID = ?",
            (grade, difficulty_new, stability_new, date_just_reviewed, date_to_review, topic_id),
        )
        conn.commit()


def topic_exists(db_path: str, topic_id: int) -> bool:
    # Return True if a topic with TopicID exists in the `topics` table.
    with _get_conn(db_path) as conn:
        cur = conn.execute("SELECT 1 FROM topics WHERE TopicID = ? LIMIT 1", (topic_id,))
        return cur.fetchone() is not None
