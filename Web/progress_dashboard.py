"""
Progress Dashboard for AI Fitness Trainer
"""
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

def load_workout_data():
    try:
        with open('workout_data/sessions.json', 'r') as f:
            return json.load(f)
    except:
        return []

def create_progress_report():
    sessions = load_workout_data()
    
    if not sessions:
        print("No workout data found. Complete some workouts first!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(sessions)
    df['date'] = pd.to_datetime(df['start_time']).dt.date
    df['duration_min'] = df['duration'] / 60
    
    print("=" * 50)
    print("📊 WORKOUT PROGRESS DASHBOARD")
    print("=" * 50)
    
    # Summary stats
    print(f"Total Workouts: {len(df)}")
    print(f"Total Reps: {df['reps'].sum()}")
    print(f"Total Calories: {df['calories'].sum():.1f}")
    print(f"Total Workout Time: {df['duration_min'].sum():.1f} minutes")
    
    # Recent workouts
    print("\n📅 Recent Workouts:")
    recent = df.tail(5)
    for _, session in recent.iterrows():
        print(f"  {session['date']} - {session['exercise']} - {session['reps']} reps")
    
    # Exercise distribution
    print("\n🎯 Exercise Distribution:")
    ex_counts = df['exercise'].value_counts()
    for ex, count in ex_counts.items():
        print(f"  {ex}: {count} sessions")

if __name__ == "__main__":
    create_progress_report()