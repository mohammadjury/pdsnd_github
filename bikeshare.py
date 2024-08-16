import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Prompts the user to select a city, month, and day for data analysis.

    Returns:
        city (str): Name of the city to analyze (e.g., 'chicago', 'new york city', 'washington').
        month (str): Name of the month to filter by, or "all" for no month filter.
        day (str): Name of the day of the week to filter by, or "all" for no day filter.
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    city = get_user_input(
        "Which city would you like to filter by? (new york city, chicago, washington)\n",
        CITY_DATA.keys()
    )
    
    month = get_user_input(
        "Which month would you like to filter by? (January, February, March, April, May, June) or type 'all' if no preference\n",
        ["january", "february", "march", "april", "may", "june", "all"]
    )
    
    day = get_user_input(
        "Which day? (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) or type 'all' if no preference\n",
        ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"]
    )
    
    return city, month, day

def get_user_input(prompt, valid_options):
    """
    Validates and returns user input based on a set of valid options.

    Args:
        prompt (str): The message to display when asking for user input.
        valid_options (list): A list of valid input options.

    Returns:
        user_input (str): The validated user input.
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        print("Invalid input. Please try again.")

def load_data(city, month, day):
    """
    Loads and filters the bikeshare data for the specified city, month, and day.

    Args:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter by, or "all" for no month filter.
        day (str): Name of the day of the week to filter by, or "all" for no day filter.

    Returns:
        df (DataFrame): Pandas DataFrame containing the filtered bikeshare data.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    
    if month != 'all':
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel based on the filtered data.

    Args:
        df (DataFrame): The filtered bikeshare data.

    Prints:
        Most Common Month, Day, and Hour of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print(f"Most Common Month: {df['month'].mode()[0].title()}")
    print(f"Most Common Day: {df['day_of_week'].mode()[0].title()}")
    df['hour'] = df['Start Time'].dt.hour
    print(f"Most Common Hour: {df['hour'].mode()[0]}")

    print(f"\nThis took {time.time() - start_time} seconds.")

def station_stats(df):
    """
    Displays statistics on the most popular stations and trips based on the filtered data.

    Args:
        df (DataFrame): The filtered bikeshare data.

    Prints:
        Most Commonly Used Start Station, End Station, and Trip Combination.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print(f"Most Commonly Used Start Station: {df['Start Station'].mode()[0]}")
    print(f"Most Commonly Used End Station: {df['End Station'].mode()[0]}")
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most Commonly Used Combination of Start and End Station Trip: {common_trip}")

    print(f"\nThis took {time.time() - start_time} seconds.")

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration based on the filtered data.

    Args:
        df (DataFrame): The filtered bikeshare data.

    Prints:
        Total Travel Time and Mean Travel Time in days and minutes respectively.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Total Travel Time: {total_travel_time / 86400:.2f} Days")
    print(f"Mean Travel Time: {mean_travel_time / 60:.2f} Minutes")

    print(f"\nThis took {time.time() - start_time} seconds.")

def user_stats(df):
    """
    Displays statistics on bikeshare users based on the filtered data.

    Args:
        df (DataFrame): The filtered bikeshare data.

    Prints:
        Count of User Types, Gender Types, and statistics on Birth Year if available.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print(f"User Types: {df['User Type'].value_counts().to_dict()}")
    
    if 'Gender' in df.columns:
        print(f"Gender Types: {df['Gender'].value_counts().to_dict()}")
    
    if 'Birth Year' in df.columns:
        print(f"Earliest Year of Birth: {int(df['Birth Year'].min())}")
        print(f"Most Recent Year of Birth: {int(df['Birth Year'].max())}")
        print(f"Most Common Year of Birth: {int(df['Birth Year'].mode()[0])}")

    print(f"\nThis took {time.time() - start_time} seconds.")

def display_raw_data(df):
    """
    Displays raw data in chunks of 5 rows based on user input.

    Args:
        df (DataFrame): The filtered bikeshare data.

    Asks:
        User if they would like to see 5 rows of raw data at a time.
    """
    start_loc = 0
    while True:
        view_data = input("Do you want to see raw data? Type 'yes' or 'no':\n").lower()
        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
        else:
            break

def main():
    """
    Main function that orchestrates the bikeshare data exploration.

    The function repeatedly prompts the user to select a city, month, and day,
    loads the filtered data, displays statistics, and offers the option to restart.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        if input('\nWould you like to restart? Enter yes or no.\n').lower() != 'yes':
            break

if __name__ == "__main__":
    main()