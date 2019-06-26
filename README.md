# investigate-a-dataset-NoShow
Project: Investigate a Dataset (noshowappointments- data set!)
Table of Contents
Introduction
Data Wrangling
Exploratory Data Analysis
Conclusions

Introduction
This dataset collects information from 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included in each row. ScheduledDay, tells us on what day the patient set up their appointment. ‘Neighborhood’ indicates the location of the hospital. ‘Scholarship’ indicates whether or not the patient is enrolled in Brasilian welfare program Bolsa Família. the data set is provided by kaggel. throughout this project we are trying to answer these questions by exploring the dataset and also the connections among variables.

Questions:
(1)Are patient who missed an appointmant befor more likly to miss the next appointment? (2)What is the no-show proportion? (3)Are no-show appointments associated with a certain gender? (4)How are weekdays affecting patients absence? (5)How is age affecting patients absence?

In order to understand the dataset we will call shape, info and describe.
So, we have 110527 appoinmements were booked and 14 columns.

We could see that the min age is -1 which is impossible! and no null values in all 14 coulmns, How lucky we are :) all columns type are okay but for AppointmentDay and ScheduledDay columns we will change it to datetime.
No duplicated rows in the data set
No null values in the data set.
# data cleaning 
We have created a function ( changeToTime) to change AppointmentDay datatype and ScheduledDay to datetime64[ns].And change the No-show column to NoShow cause I have got a problem each time I deal with. Also I add new colunms hour_scheduled,day_scheduled, day_appointment where they determine the hour of scheduled, week day name of ScheduledDay and week day name of AppointmentDay ,respectively.
We have deleted the row where -1 value in age.

To make the data more Understandable and easy to deal with, We have changed the No, yes values in the data set to 0,1.
We have added a new column AppointmentsMissed which sums how many has the patient been absent. I would like to see if there is a relation between NoShow and AppointmentsMissed.

#Exploratory Data Analysis
Research Question 1 (Are patient who missed an appointmant befor more likly to miss the next appointment?)
Since the correlation is 0.58 , that means there is a possitive relationship between NoShow and AppointmentsMissed
Research Question 2 (What is the no-show proportion?)
20.2% of appointments were missed.
Research Question 3 (Are no-show appointments associated with a certain gender?)
As shown in the plot , Female are more expected to not show with proportion 65.4% That is maybe because of their busy life.
