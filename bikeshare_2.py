import time

import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'newyorkcity': 'new_york_city.csv', #original key --> new york city ; changed to avoid an error with the spaces
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday','thursday','friday','saturday','sunday']

def pause():
    """
    Function to stop the execution of the program for visualising the analysis step by step.     
    """
    programPause = input("Press the <ENTER> key to continue...")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_city = False
    valid_month = False
    valid_day = False
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while not valid_city:
        city = input('\nPlease insert a valid city (Chicago, New York City, Washington)\n').lower().replace(' ','')
        if city in CITY_DATA:
            valid_city = True
        else:
            print('\nInvalid input!. We do not have any records for the selected city or there is a typing error.\n')
    
    # get user input for month (all, january, february, ... , june)
    
    while not valid_month:
        month = input('\nSelect a month to filter by (from january to june) or enter all to show all records:\n').lower()      
        if month in months or month == 'all':
            valid_month = True
        else: 
            print('\nInvalid input!. We do not have any records for the selected month or there is a typing error.\n')
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    while not valid_day:
        day = input('\nSelect a day to filter by (Monday to Sunday) or enter all for all records:\n').lower()
        if  day in days or day == 'all':
            valid_day = True
        else: 
            print('\nInvalid input!. We do not have any records for the selected day or there is a typing error.\n')

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        
        month = months.index(month)+1
        
        # filter by month to create the new dataframe
        df = df[df['month']==month] 

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()] 
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month = months[common_month-1]
    print('\nThe most common month is: {}\n'.format(common_month.capitalize()))
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of week is: {}\n'.format(common_day))
    # display the most common start hour
    common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print('\nThe most common start hour is: {}h\n'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    pause()


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0] 
    print('\nThe most used start station for the selected parameters is: {}\n'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0] 
    print('\nThe most used end station for the selected parameters is: {}\n'.format(common_end_station))
    
    # display most frequent combination of start station and end station trip
    most_frequent_combination = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print('\nThe most frequent combination of start and end station is: {}\n'.format(most_frequent_combination))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    pause()


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nThe total travel time is: {}\n'.format(total_travel_time))
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe average travel time is: {}\n'.format(mean_travel_time))
       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    pause()


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    count_user_type = df['User Type'].value_counts()

    #print('\nThe count of user per type is: {} \n', count_user_type)
    print('\nThe count of user per type is: {} \n'.format(count_user_type))
   
    # Display counts of gender
    if city == 'washington':
        print('\nSorry! We do not have any gender records for Washington\n')
    else:
        user_gender_count=df['Gender'].value_counts()
        print('\nThe count of user per sex gender is: \n', user_gender_count)

        # Display earliest, most recent, and most common year of birth    
        early_birth_year = df['Birth Year'].min()
        print('\nThe earliest user\'s Birth Year is: {}\n'.format(int(early_birth_year)))
        recent_birth_year = df['Birth Year'].max()
        print('\nThe most recent user\'s Birth Year is: {}\n'.format(int(recent_birth_year)))
        common_birth_year = df['Birth Year'].mode()[0]
        print('\nThe most common user\'s Birth Year is: {}\n'.format(int(common_birth_year)))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    pause()

def raw_data(df):
    ''' Your docstring here '''
    i = 0
    raw = input('Would you like to see some data from the dataset? Type: Yes or No.').lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input('Display 5 adittional lines. Type: Yes/No.').lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()