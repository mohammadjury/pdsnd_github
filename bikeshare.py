import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = get_user_input("Which city would you like to filter by? new york city, chicago or washington?\n", 
                          ["new york city", "chicago", "washington"])
    
    month = get_user_input("Which month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n", 
                           ["january", "february", "march", "april", "may", "june", "all"])
    
    day = get_user_input("Are you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n", 
                         ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"])
    
    return city, month, day

def get_user_input(prompt, valid_options):
    """
    Helper function to get user input and validate it against a list of valid options.
    
    Args:
        (str) prompt - input prompt for the user
        (list) valid_options - list of valid options for the user input
    
    Returns:
        (str) user_input - validated user input
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        print("Sorry, I didn't catch that. Try again.")

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A').str.lower()
    
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Most Common Month:", df['month'].mode()[0])
    print("Most Common Day:", df['day_of_week'].mode()[0])
    df['hour'] = df['Start Time'].dt.hour
    print("Most Common Hour:", df['hour'].mode()[0])

    print(f"\nThis took {time.time() - start_time} seconds.")

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("Most Commonly Used Start Station:", df['Start Station'].mode()[0])
    print("Most Commonly Used End Station:", df['End Station'].mode()[0])
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most Commonly Used Combination of Start and End Station Trip:", common_trip)

    print(f"\nThis took {time.time() - start_time} seconds.")

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Total Travel Time: {total_travel_time / 86400:.2f} Days")
    print(f"Mean Travel Time: {mean_travel_time / 60:.2f} Minutes")

    print(f"\nThis took {time.time() - start_time} seconds.")

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User Types:", df['User Type'].value_counts().to_dict())
    if 'Gender' in df.columns:
        print("Gender Types:", df['Gender'].value_counts().to_dict())
    if 'Birth Year' in df.columns:
        print("Earliest Year of Birth:", int(df['Birth Year'].min()))
        print("Most Recent Year of Birth:", int(df['Birth Year'].max()))
        print("Most Common Year of Birth:", int(df['Birth Year'].mode()[0]))

    print(f"\nThis took {time.time() - start_time} seconds.")

def display_raw_data(df):
    """Displays raw data upon user request."""
    start_loc = 0
    while True:
        view_data = input("Do you want to see raw data? Type 'yes' or 'no':\n").lower()
        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

