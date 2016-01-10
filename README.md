## Welcome

### Movie Scheduling App

#### Business Rules and Assumptions:

1.  The theater has one available screen per movie.
2.  The schedule should repeat each movie as many times as possible during the hours of opertation. 
3.  A movie cannot end after the theater closing time. 
4.  All theaters close before midnight.
5.  When the theater opens it takes one hour to setup the theater before any movies can be shown. 
6.  Theater cleanup, change over work, and previews require a combined 35 minutes between the end of one showtime and the start of the next. 
7.  Movies should be scheduled as late as possible so the prime-time evening hours are maximized. 
8.  Even though the theater is open and ready in the morning, the early hours are the least busy and therefore scheduled last. 
9.  Show times should start at easy to read times (2:35 is preferred to 2:37, for example).

Input assumption - comma delimiters will not appear anywhere in the data values (no movie titles with commas, for example). Movie information will be in csv file in the following format: 
Movie Title, Release Year, MPAA Rating, Run Time. 

#### Prelimary Design Decisions

Since the spec states that this program may be rolled out to other movie theaters, I decided to use a configuration file to setup items like theater opening and closing time--anything that could vary by locations. 

Since this is new development and none of the features required Python 2 compatible libraries, I decided to use Python 3.4.2

#### Dependencies

PyYAML is required to run the program. PyYAML may be installed using
 
```pip install pyyaml```

#### Program Execution

Run the following command at the command line:

```python app.py movies.csv```

Additional test files must be in the same directory as app.py
 
#### Misc

I welcome any and all feedback to improve the program. Thanks!
 


