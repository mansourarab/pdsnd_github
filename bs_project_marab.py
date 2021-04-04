import pandas as pd
import datetime as dt
import time
import calendar

#Extraction Data Function
def extraction_fun(city,fmonth,fday):
    CITY_DATA = { 'Chicago': 'chicago.csv',
              'New york': 'new_york_city.csv',
              'Washington': 'washington.csv' }
    
    #Loding the data into a data frame
    city_df = pd.read_csv(CITY_DATA[city])
    
    
    #Cleaning the data frame from NULL values
    city_df.fillna(method = 'ffill', axis = 0)
    
    #Parsing the 'Start Time' to datetime object
    city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])

    #Extract month from Start Time to create new column (Month)
    city_df['Months Num'] = city_df['Start Time'].dt.month
    month_names = list(calendar.month_name)
    months = []
    for i in city_df['Months Num']:
        months.append(month_names[i])
    city_df.drop(['Months Num'] , axis =1 , inplace = True)
    city_df.insert(7 , 'Months' , months, allow_duplicates = True)
    
    #Extract day of week from Start Time to create new column (Week Day)
    city_df['Week Days Num'] = city_df['Start Time'].dt.dayofweek 
    week_days_names = list(calendar.day_name)
    week_days = []
    for i in city_df['Week Days Num']:
        week_days.append(week_days_names[i])


    city_df.drop(['Week Days Num'] , axis =1 , inplace = True)
    city_df.insert(8 , 'Week Days' , week_days, allow_duplicates = True)
    
    #Filtering Part for Month
    if fmonth != 'All':
        fmonth_index = month_names.index(fmonth)
        fmonth = month_names[fmonth_index]
        # filter by month to create the new dataframe
        city_df = city_df[city_df['Months'] == fmonth]
        
        
        
    #Filtering Part for Week Day
    if fday != 'All':
        fday_index = week_days_names.index(fday)
        fday = week_days_names[fday_index]
        # filter by day of week to create the new dataframe
        city_df = city_df[city_df['Week Days'] == fday]
        
    
        
    return city_df

#///////////////////////////////////////////////////////////////////////////////////////

#This function is to compute the First calculations: Most popular hour,and the counts of trips
def pop_times_traviling(df):
    
    #The most popular month
    mpm_mode = df['Months'].mode()[0]
    print('The most popular month to travel is: {}\n'.format(mpm_mode))
        #The counts of trips
    counter = df['Months'].value_counts()
    print('The count for the trips in the requested period is: {}'.format(counter[mpm_mode]))
    print('..........\n >>>>>>>>>\n .........')
    
    #The most popular day of week
    mpd_mode = df['Week Days'].mode()[0]
    print('The most popular day of the week to travel is: {}\n'.format(mpd_mode))
        #The counts of trips
    counter = df['Week Days'].value_counts()
    print('The count for the trips in the requested period is: {}'.format(counter[mpd_mode]))
    print('..........\n >>>>>>>>>\n .........')
   
    #The most popular hour
    df['Hours'] = df['Start Time'].dt.hour
    mph_mode = df['Hours'].mode()[0]
    print('The most popular hour in the day is: {}\n'.format(mph_mode))
        #The counts of trips
    counter = df['Hours'].value_counts()
    print('The count for the trips in the requested period is: {}'.format(counter[mph_mode]))
    print('..........\n >>>>>>>>>\n .........')
    df.drop(['Hours' , 'Months'] , axis = 1 , inplace = True)
    return

#///////////////////////////////////////////////////////////////////////////////////////

#This function is to compute the Second calculations: Most popular stations and Trips
def pop_stations(df):
    
    #The most popular Start Station
    mpss_mode = df['Start Station'].mode()[0]
    print('The most popular Start point is: {}\n'.format(mpss_mode))
    
    #The most popular End Station
    mpes_mode = df['End Station'].mode()[0]
    print('The most popular end point is: {}\n'.format(mpes_mode))
    
    #The most popular Trip
    mpt_mode = ('from ' + df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('The most popular Trip is: {}\n'.format(mpt_mode))
    return

#///////////////////////////////////////////////////////////////////////////////////////

#This function is to compute the Third calculations: Total Travilling Time, and Average Travilling Time
def travil_calcs(df):
    
    # Total Travil Time
    tot_travil_sec = df['Trip Duration'].sum()
    tot_travil_mins = tot_travil_sec / 60
    print('The Total Travil Time (in minutes) is: {}\n '.format(tot_travil_mins))
    
    # Avg Travil Time
    avg_travil_sec = df['Trip Duration'].mean()
    avg_travil_mins = avg_travil_sec / 60
    print('The Average Travil Time (in minutes) is: {}\n '.format(avg_travil_mins))
    return

#///////////////////////////////////////////////////////////////////////////////////////

#This function is to compute the Fourth calculations: The Counts of user types, thier gender (only NYC and Chicago), Common year of birth

def user_info(df , city):
    #User Types Counter
    print('The user types count is: ')
    print(df['User Type'].value_counts())
    print('\n')
    
    #Gender Counter
    if city == 'Washington':
        print('No Data are available for Gender and Birth!')
    
    
    else:
        print('The gender types count is: ')
        print(df['Gender'].value_counts())
        print('\n')
        
        #Birth Year Calculations
        '''The Earliest Year'''
        by_min = int(df['Birth Year'].min())
        print('The earliest year is:{} \n'.format(by_min))
        
        '''The Most Recent Year'''
        by_max = int(df['Birth Year'].max())
        print('The Most Recent year is: {} \n'.format(by_max))
        
        '''The Most Common Year'''
        by_mode = int(df['Birth Year'].mode()[0])
        print('The Most Common Birth year is: {} \n'.format(by_mode))
    return

#///////////////////////////////////////////////////////////////////////////////////////

#This function is to display (5) rows of raw data at a time
def raw_data(df):
    count = 0
    sample = print(df.sample(5))
    pd.set_option('display.max_columns',200)
    return sample

#///////////////////////////////////////////////////////////////////////////////////////

#The main Function
#This project is to show data regarding bikeshare program!
def main():
        print('Welcome to BikeShare Data Center!')
        
        
        count = 0
        while True:
            try:
                if count != 0:
                    quit()
                city = input('I Would like to get some data about: chicago , washington , new york   ').capitalize()
                fday = input('I would like to filter the data by (full day name): (Type \'all\' if no filter is needed)   ').capitalize()
            
            #The last Six months information are not provided
                while True:
                    try:
                        fmonth = input('I would like to filter the data by (full month name): Type \'all\' if no filter is needed)   ').capitalize()
                        last_months = list(calendar.month_name[7::])
                        if fmonth in last_months:
                            print('\n No Data Available for the requested month \n')
                            del city, fday, fmonth
                            main()
                            break
                        
                        else:
                            break
                    except:
                        print('\n Month Data not available \n')
            
                    
                    
                
                
                city_df = extraction_fun(city,fmonth,fday)
                print('\n Please wait...popular times of traviling are being calculated....\n')
                time.sleep(5)
                print('.....\n')
                pop_times_traviling(city_df)
                print('.....\n')
                print('\\\\\\\\\\')
                

                print('Please wait...popular destinations for traviling are being calculated....\n')
                time.sleep(5)
                print('.....\n')
                pop_stations(city_df)
                print('.....\n')
                print('\\\\\\\\\\')

                print('Please wait...time statistics for traviling are being calculated....\n')
                time.sleep(5)
                print('.....\n')
                travil_calcs(city_df)
                print('.....\n')
                print('\\\\\\\\\\')

                print('Please wait...user information are being calculated....\n')
                time.sleep(5)
                print('.....\n')
                user_info(city_df , city)
                print('.....\n')
                print('\\\\\\\\\\')
                
                print('Calculations are done!')
                
                
            #Call for raw data
                while True:
                    try:
                        raw_data_choise = input('Would you like to see a raw data sample? (Y/N)\n').capitalize()
                        if raw_data_choise =='Y':
                            print('Alright! Preparing raw data.....\n')
                            raw_data_sample = raw_data(city_df)
                            time.sleep(3)
                            print(raw_data_sample)
                            
                        elif raw_data_choise == 'N':
                            break
                    except:
                        print('\n Invalid input! please enter a correct value! \n ')
            
            
            #Restarting the Program
                while True:
                    try:
                        restart_choise = input('Do you want to do another analysis? (Y/N)\n').capitalize()
                        if restart_choise =='Y':
                            print('Alright!')
                            main()
                            
                        elif restart_choise == 'N':
                            print('Sure! See you again!')
                            count +=1
                            quit()
                            break
                    except:
                        print('\n Invalid input! please enter a correct value! \n ')
           
                break     
            except:
                print('\n Invalid input! Please enter correct information \n')
                del city , fmonth, fday
                
main()