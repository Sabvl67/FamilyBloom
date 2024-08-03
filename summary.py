import pandas as pd
import os
import collections
import matplotlib.pyplot as plt
import seaborn as sns

# Set a light beige color theme with soft colors
sns.set_theme(style="whitegrid")
custom_palette = sns.color_palette("pastel", n_colors=3)

# Print the current working directory
print("Current Working Directory:", os.getcwd())

# List files in the current directory to confirm the upload
print("Files in Current Directory:", os.listdir())

# Load the CSV file
csv_file_path = '/Users/PC/Desktop/AlbertaHealth/mood_tracking_multiple_entries.csv'
df = pd.read_csv(csv_file_path)

# Display the DataFrame
print(df)

# Count the occurrences of each mood
mood_counts = df['mood'].value_counts()
print("\nMood Counts:")
print(mood_counts)

# Filter and display the times when the user is mad
mad_times = df[df['mood'] == 'mad'][['time', 'description']]
print("\nTimes and Descriptions when the user is mad:")
print(mad_times)

# Filter and display the times when the user is happy
happy_times = df[df['mood'] == 'happy'][['time', 'description']]
print("\nTimes and Descriptions when the user is happy:")
print(happy_times)

# Filter and display the times when the user is sad
sad_times = df[df['mood'] == 'sad'][['time', 'description']]
print("\nTimes and Descriptions when the user is sad:")
print(sad_times)

# Analyze the descriptions to find common catalysts for the moods
def find_common_catalysts(descriptions):
    word_counter = collections.Counter()
    for description in descriptions:
        words = description.lower().split()
        word_counter.update(words)
    return word_counter.most_common()

# Find common catalysts for being sad, happy, and mad
sad_descriptions = df[df['mood'] == 'sad']['description']
happy_descriptions = df[df['mood'] == 'happy']['description']
mad_descriptions = df[df['mood'] == 'mad']['description']

common_catalysts_sad = find_common_catalysts(sad_descriptions)
common_catalysts_happy = find_common_catalysts(happy_descriptions)
common_catalysts_mad = find_common_catalysts(mad_descriptions)

print("\nCommon Catalysts for being Sad:")
print(common_catalysts_sad)

print("\nCommon Catalysts for being Happy:")
print(common_catalysts_happy)

print("\nCommon Catalysts for being Mad:")
print(common_catalysts_mad)

# Plot the mood counts
plt.figure(figsize=(10, 6))
sns.barplot(x=mood_counts.index, y=mood_counts.values, palette=custom_palette, hue=mood_counts.index, dodge=False)
plt.title('Mood Counts')
plt.xlabel('Mood')
plt.ylabel('Count')
plt.show()

# Plot the mood over time
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)
plt.figure(figsize=(12, 6))
df['mood'].resample('D').count().plot(color=custom_palette[0])
plt.title('Moods Over Time')
plt.xlabel('Date')
plt.ylabel('Count')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()

# Heatmap of mood occurrences by hour of the day
df['hour'] = df.index.hour
mood_hourly_counts = pd.crosstab(df['hour'], df['mood'])

plt.figure(figsize=(12, 8))
sns.heatmap(mood_hourly_counts, cmap=sns.light_palette("beige", as_cmap=True), annot=True, fmt='d', cbar=False)
plt.title('Mood Occurrences by Hour of the Day')
plt.xlabel('Mood')
plt.ylabel('Hour of the Day')
plt.show()

# Pairplot to visualize relationships between moods and time-related features
df['day_of_week'] = df.index.dayofweek
df['day'] = df.index.day

plt.figure(figsize=(12, 8))
sns.pairplot(df, hue='mood', palette=custom_palette)
plt.show()
