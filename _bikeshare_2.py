import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHi there! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWhich city would you like to explore: Chicago, New York City, or Washington?\nEnter the city name: ').lower()

    while city not in ['chicago', 'new york city', 'washington']:
        city = input('\nOops, that entry is not an option. Please enter Chicago, New York City, or Washington:\n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('\nWould you like to filter by month or look at all months (no month filter)? Enter the full name of the month, or enter "all" if all months:\n').lower()

    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('\nOops, that entry is not an option. Please enter a different month:\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nWould you like to filter by a day of the week or look at all days (no day filter)? Enter the day of the week, or enter "all" for all days:\n').lower()

    while day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        day = input('\nOops, that entry is not an option. Please enter a day of the week:\n').lower()

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from the Start Time column to create an hour column
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel:
        Most Frequent month
        Most Frequent day of the week
        Most Frequent hour of day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent Day of Week: ', popular_day)

    # display the most common start hour
    popular_hour = df['start_hour'].mode()[0]
    print('Most Frequent Hour of Day: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startstation = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ', popular_startstation)

    # display most commonly used end station
    popular_endstation = df['End Station'].mode()[0]
    print('Most Popular End Station: ', popular_startstation)

    # display most frequent combination of start station and end station trip
    df['Trip'] = 'From:' + ' ' + df['Start Station'] + ' ' + 'To:' + ' ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most Popular Trip: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel_time'] = df['End Time'] - df['Start Time']

    total_travel_time = df['travel_time'].sum()

    print('Total Travel Time: ', total_travel_time)

    # display mean travel time
    mean_travel_time = str(df['travel_time'].mean())
    print('Mean Travel Time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Counts:')
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Display counts of gender
        print('\nGender Counts:')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('\nBirth Year Stats:')
        min_birth_year = int(df['Birth Year'].min())
        print('The Earliest Birth Year: ', min_birth_year)

        max_birth_year = int(df['Birth Year'].max())
        print('The Most Recent Birth Year: ', max_birth_year)

        common_birth_year = int(df['Birth Year'].mode()[0])
        print('The Most Common Birth Year: ', common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Provides user the option to display raw data.
    The first 5 rows are displayed if the user enters 'yes'.
    The user has the option to keep continuing. If so, 5 more lines of data are displayed.
    """
    rowstart = 0
    rowend = 5

    seeRawData = input('\nWould you like to view the raw data? Enter yes or no:\n').lower()

    if seeRawData == 'yes':
        while rowend <= df.shape[0]:
            print(df[rowstart: rowend])
            rowstart += 5
            rowend += 5

            moreRawData = input('\nWould you like to see five more rows of raw data? Enter yes or no:\n').lower()
            if moreRawData != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no:\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
