import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ["chicago", "washington", "new york city"]
months = ["january", "february", "march", "april", "may", "june", "all"]
days = ["all", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter a city name (chicago, new york city, washington): ").lower()
        if city in cities:
            break
        else: print("Invalid input. Please try again!")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter a month (all, january, february, [up to june]): ").lower()
        if month in months:
            break
        else: print("Invalid input. Please try again!")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter a day of the week (all, sunday, monday, .. saturday: ").lower()
        if day in days:
            break
        else: print("Invalid input. Please try again!")

    print('-'*40)
    return city, month, day


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
    #loading file, converting, extracting
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    #filtering by month
    if month != "all":
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    #filtering by day
    if day != "all":
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    com_month = df['month'].mode()[0]
    print("Most common month: ", com_month)

    # TO DO: display the most common day of week
    com_day = df['day_of_week'].mode()[0]
    print("Most common day of the week: ", com_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    com_hour = df['hour'].mode()[0]
    print("Most common start hour: ", com_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    com_ss = df['Start Station'].value_counts().index.tolist()[0]
    print("Most commonly used start station:", com_ss)

    # TO DO: display most commonly used end station
    com_es = df['End Station'].value_counts().index.tolist()[0]
    print("Most commonly used end station:", com_es)

    # TO DO: display most frequent combination of start station and end station trip
    freq_comb = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print("Most frequent combination of start and end station trip:", freq_comb.index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time:", total_time, "seconds.")

    # TO DO: display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("Mean travel time:", avg_time, "seconds.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
        
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # takes city as input - washington does not have gender/birth records
    if city == "washington":
        print("No gender and birth year records are available for Washington, DC.")
        
    else:
        # TO DO: Display counts of user types
        user_types = df['User Type'].value_counts()

        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()

        # TO DO: Display earliest, most recent, and most common year of birth
        birthdays = df['Birth Year'].sort_values()
    
        recent_birth = int(birthdays[0])
        early_birth = int(birthdays.min())
        comm_birth = int(birthdays.mode()[0])
        
        print("Most recent birth:", recent_birth,
              "\nEarliest birthday:", early_birth,
              "\nMost common year of birth:", comm_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        #prompting user to view raw data
        read_data = True
        i = 0
        while read_data == True:
            raw = input("Would you like to view 5 lines of raw data? (y/n) ").lower()
            if raw == "y":
                print(df.iloc[i:i+5])
                i = i + 5
            elif raw == "n":
                read_data = False
            else:
                print("Invalid input. Please try again.")
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
