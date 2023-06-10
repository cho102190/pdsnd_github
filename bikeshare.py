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
    print('Hi! Let\'s explore some US bikeshare data! Hallo! Lassen wir daten über Bikeshare programme in den USA entdecken!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ['chicago','new york city','washington']
        city = input ("Which city would you like to look into? Please type among Chicago, New York City, and Washington.").lower()
        if city in cities:
            break
        else:
            print ("Please enter a city name as it appears above.")

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['All','Jan','Feb','Mar','Apr','May','Jun']
        month = input ("Which month would you like to analyze? Please type among Jan, Feb, Mar, Apr, May, and Jun. If you would not like to filter the data, then type 'All'.")
        if month in months:
            break
        else:
            print ("Please enter the month as it appears above.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['All','Mon','Tue','Wed','Thu','Fri','Sat', 'Sun']
        day = input ("Which day would you like to analyze? Please type among Mon, Tue, Wed, Thu, Fri, Sat, and Sun. If you would not like to filter the data, then type 'All'.")
        if day in days:
            break
        else:
            print ("Please enter the day as it appears above :)")


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
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'All':
        df = df[df['month'].str.startswith(month.title())]
   
    if day != 'All':
        df = df[df['day_of_week'].str.startswith(day.title())]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    most_common_month = df['month'].mode()[0]
    print ('Most common month:', most_common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_common_day = df['day_of_week'].mode()[0]
    print ('Most common day:', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_starthour = df['hour'].mode()[0]
    print ('Most common start hour:', most_common_starthour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print ("The most common start station: ", start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print ("The most common end station: ", end_station)

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station']).count()
    print("The most frequently used combination of start station and end station trip: ", start_station, " & ", end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    minute,second=divmod(total_travel_time,60)
    hour,minute=divmod(minute,60)
    print("The total travel time: {} hour(s) {} minute(s) {} second(s)".format(hour,minute,second))

    # display mean travel time
    avg_travel_time = round(df['Trip Duration'].mean())
    m,sec = divmod(avg_travel_time,60)
    if m>60:
          h,m = divmod(m,60)
          print ("The total travel time: {} hour(s) {} minute(s) {} second(s)".format(h,m,sec))
    else:
          print ("The total travel time: {} minute(s) {} second(s)".format(m,sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type)

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    except KeyError:
        print("Gender: Data is not available.")
    

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = df['Birth Year'].min()
        most_recent_year_of_birth = df['Birth Year'].max()
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print("The earliest year of birth: ", earliest_year_of_birth,
          ", the most recent year of birth: ", most_recent_year_of_birth,
          ", and the most common year of birth: ", most_common_year_of_birth)
    except:
        print ("Data is not available for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
    return df
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
