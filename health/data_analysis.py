import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
from health import app
from health.models import Workout

GRAPH_DIR = os.path.join(os.path.dirname(__file__), 'static', 'graphs')

def load_workouts_as_dataframe():
    with app.app_context():
        workouts = Workout.query.all()
        data = {
            'Date': [workout.date for workout in workouts],
            'Workout Type': [workout.workout_type for workout in workouts],
            'Duration (minutes)': [workout.duration for workout in workouts],
            'Calories Burned': [workout.calories for workout in workouts]
        }
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df = df.sort_values(by='Date')
        return df

def plot_workouts_per_day(df):
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df.set_index('Date', inplace=True)

    # Подсчёт тренировок по дням
    workouts_per_day = df.resample('D').count()['Workout Type']  # Подсчёт только для дней с тренировками
    workouts_per_day = workouts_per_day.asfreq('D', fill_value=0)  # Заполнение дней без тренировок нулями

    plt.figure(figsize=(12, 6))
    workouts_per_day.plot(title='Number of Workouts per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Workouts')
    plt.grid(True)
    plt.tight_layout()
    filepath = os.path.join(GRAPH_DIR, 'workouts_per_day.png')
    plt.savefig(filepath)
    plt.close()


def plot_calories_burned(df):
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df.set_index('Date', inplace=True)

    # Подсчет суммы калорий по дням
    calories_burned = df['Calories Burned'].groupby(df.index.date).sum()

    plt.figure(figsize=(15.6, 7.8))
    plt.plot(calories_burned.index, calories_burned, marker='o', linestyle='-')
    plt.title('Calories Burned over Time')
    plt.xlabel('Date')
    plt.ylabel('Calories Burned')
    plt.grid(True)
    plt.tight_layout()
    filepath = os.path.join(GRAPH_DIR, 'calories_burned.png')
    plt.savefig(filepath)
    plt.close()

def analyze_workouts(workouts_df):
    recommendations = []
    if workouts_df.resample('W', on='Date').size().mean() < 3:
        recommendations.append("It is recommended to increase the frequency of workouts to at least 3 times per week.")
    if workouts_df['Duration (minutes)'].mean() < 30:
        recommendations.append("Consider increasing your average workout duration to 30 minutes or more.")
    if len(workouts_df['Workout Type'].unique()) < 5:
        recommendations.append("Add variety to your training process by including new types of activities.")
    if workouts_df['Calories Burned'].sum() < 1000:
        recommendations.append("Increase the intensity of your workouts to boost the total number of calories burned.")
    return recommendations


if __name__ == "__main__":
    df = load_workouts_as_dataframe()
    if not df.empty:
        plot_workouts_per_day(df)
        plot_calories_burned(df)
