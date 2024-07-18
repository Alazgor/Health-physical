import matplotlib.pyplot as plt
import pandas as pd
import os
from io import BytesIO
from flask import send_file

# Absolute path to dir static/graphs
GRAPH_DIR = os.path.join(os.path.dirname(__file__), 'static', 'graphs')


def load_workouts_as_dataframe():
    from health.models import Workout
    workouts = Workout.query.all()
    data = {
        'Date': [workout.date for workout in workouts],
        'Workout Type': [workout.workout_type for workout in workouts],
        'Duration (minutes)': [workout.duration for workout in workouts],
        'Calories Burned': [workout.calories for workout in workouts]
    }
    df = pd.DataFrame(data)
    return df


def plot_workouts_per_day(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    workouts_per_day = df.resample('D').size()
    plt.figure(figsize=(12, 6))
    workouts_per_day.plot(title='Number of Workouts per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Workouts')
    plt.grid(True)
    plt.tight_layout()

    # Сохраните график в BytesIO
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    return img_bytes


def plot_calories_burned(df):
    df['Date'] = pd.to_datetime(df['Date'])
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Calories Burned'], marker='o', linestyle='-')
    plt.title('Calories Burned over Time')
    plt.xlabel('Date')
    plt.ylabel('Calories Burned')
    plt.grid(True)
    plt.tight_layout()

    # Сохраните график в BytesIO
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    return img_bytes
