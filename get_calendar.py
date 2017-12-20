#!/usr/bin/env python

from icalendar import Calendar, Event
import datetime
import urllib2

import requests
import bs4

import json
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

import time
from datetime import timedelta






  
def get_ics_url(url):
            
    ''' 
    inputs URL of page containing .ics calendar
    outputs URL of .ics file
    '''    

    
    # case 1: html-generated content
    
    page = requests.get(url).content
    soup = bs4.BeautifulSoup(page, 'lxml')

    links = soup.find_all('a', {'href' : re.compile('.*\.ics') })
    
    for link in links:
            
        if link.get('href') != None and '.ics' in link.get('href'):
            endout = link.get('href')
            
            if endout[:6] == 'webcal':
                endout ='https' + endout[6:]
            print
            print 'URL: ' + endout
            print
            return endout
        break

    

    
    # case 2: javascript-generated content
    
    driver = webdriver.Chrome()
    driver.get(url)

    wait(driver, 10).until                                                                      (EC.frame_to_be_available_and_switch_to_it("trumba.spud.1.iframe"))

    element = driver.find_element_by_xpath('//a[contains(@href, ".ics")]')
    myHrefVal = element.get_attribute('href')
    
    print
    print 'URL: ' + myHrefVal
    print 
    return myHrefVal
    
    







def write_file(ics_url, set_calendar_name):
    
    '''
    inputs URL of .ics file and intended calendar name
    outputs .ics file saved as set_calendar_name
    '''


    url = ics_url

    response = urllib2.urlopen(url)
    webContent = response.read()

    f = open(set_calendar_name, 'w')
    f.write(webContent)
    f.close

    print 'File name: ' + set_calendar_name
    print
    return set_calendar_name
    









def get_calendar(file, dict_format_type):
    
    '''
    inputs .ics file and dictionary value format type: 'full' or 'abbrev'
    
    sample full dictionary: 
    {'Pre-Health Interview Tips & Tactics': 'August 28, 2017'}
    
    sample abbrev dictionary: 
    {'Pre-Health Interview Tips & Tactics': '08/28/17'}
        
    outputs dictionary of events w/ keys as event names and values as dates
    '''

    
    d = {}


    g = open(file,'rb')
    gcal = Calendar.from_ical(g.read())

    for component in gcal.walk():
        
        if component.name == "VEVENT":

            print 'Events: '
            print
            print component.get('summary')
            print component.get('dtstart').dt
            #print component.get('dtend').dt
            #print component.get('dtstamp').dt
    
            summary = (component.get('summary')).encode('utf-8')

            startDate = str(component.get('dtstart').dt)
            startDate = startDate[0:10]
            dt = datetime.datetime.strptime(startDate, '%Y-%m-%d')
            # can convert back to string 
            # date is currently in proper datetime format

            
            
            if dict_format_type == 'full': 
                newDate = dt.strftime('%B %d, %Y')
                d[summary] = newDate 
            

            if dict_format_type == 'abbrev':
   
                newDate = dt.strftime('%m/%d/%y')
                d[summary] = newDate

            

    g.close()

    print
    print 'All events: '
    print
    print d
    print
    return d
    











def get_events(time_input, num_d):
#def get_events(time_input):   
    
    '''
    inputs time keyword and numerical dictionary
    time_input contains 'today', 'tomorrow', 'this week', 'next week',
        'this month', 'next month', or form 'mm/dd/yy'
    outputs dictionary of events meeting time requirement
    '''

    
    sorted_dict = {}
    


    ### time_input cases

    # case 1: 'today'    
    if 'today' in time_input.lower():
    
        today_date = (time.strftime("%m/%d/%y"))
        #today_date = datetime.date.today()

        for key in num_d:
            if num_d[key] == today_date:
                sorted_dict[key] = today_date


    

    
    # case 2: 'tomorrow'
    if 'tomorrow' in time_input.lower():
    
        tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)        
        tomorrow_date = tomorrow_date.strftime("%m/%d/%y")

        for key in num_d:
            if num_d[key] == tomorrow_date:
                sorted_dict[key] = tomorrow_date
    
    



    
    # case 3: 'this week'
    if 'this week' in time_input.lower():

        for key in num_d:
            
            today = datetime.datetime.today().date()
            date_compare = datetime.datetime.strptime(num_d[key], '%m/%d/%y').date()
            
            monday1 = (today - timedelta(days=today.weekday()))
            monday2 = (date_compare - timedelta(days=date_compare.weekday()))
            
            if (monday2 - monday1).days / 7 == 0:
 
                thisDate = datetime.datetime.strptime                                                       (num_d[key], '%m/%d/%y').strftime('%m/%d/%y')
                
                sorted_dict[key] = thisDate






    
    # case 4: 'next week'    
    if 'next week' in time_input.lower():
  
        for key in num_d:      

            today = datetime.datetime.today().date()
            date_compare = datetime.datetime.strptime(num_d[key], '%m/%d/%y').date()

            monday1 = (today - timedelta(days=today.weekday()))
            monday2 = (date_compare - timedelta(days=date_compare.weekday()))
 
            if (monday2 - monday1).days / 7 == 1:
 
                thisDate = datetime.datetime.strptime                                                       (num_d[key], '%m/%d/%y').strftime('%m/%d/%y')
                
                sorted_dict[key] = thisDate






    # case 5: 'this month' 
    if 'this month' in time_input.lower():

        for key in num_d:

            date_compare =                                                                              datetime.datetime.strptime(num_d[key], "%m/%d/%y").date().month
            today = datetime.datetime.today().month

            if date_compare - today == 0:
                
                thisDate = datetime.datetime.strptime                                                       (num_d[key], '%m/%d/%y').strftime('%m/%d/%y')
                
                sorted_dict[key] = thisDate





    # case 6: 'next month'
    if 'next month' in time_input.lower():
        
        for key in num_d:

            date_compare =                                                                              datetime.datetime.strptime(num_d[key], "%m/%d/%y").date().month          
            today = datetime.datetime.today().month

            if date_compare - today == 1 or date_compare - today == -11:
                
                thisDate = datetime.datetime.strptime                                                       (num_d[key], '%m/%d/%y').strftime('%m/%d/%y')
                
                sorted_dict[key] = thisDate
    
 




    # case 7: form 'mm/dd/yy'    
    for key in num_d:
        
        if num_d[key] in time_input:

            sorted_dict[key] = num_d[key]       
    

    ### end time_input cases

    print 'Matching events: '
    print
    print sorted_dict
    print
    return sorted_dict









if __name__ == '__main__':
    #get_events()

    




    
    # Harvard

    #get_calendar(write_file(get_ics_url('https://meded.hms.harvard.edu/calendar'), 'harvard_cal.ics'))
    



    #get_ics_url('https://registrar.fas.harvard.edu/calendar')
    #get_calendar(write_file(get_ics_url('https://registrar.fas.harvard.edu/calendar'), 'harvard_cal2.ics'), 'abbrev')
    


    # Chapel Hill!


    #get_ics_url('https://careers.unc.edu/calendar')
    #get_calendar(write_file(get_ics_url('https://careers.unc.edu/calendar'), 'carolina_cal.ics'))

    #print datetime.date.today()
    

    #get_events('What is today?')
    #get_events('What are events Tomorrow?')
    #get_events('What is this week')
    #get_events('what is next week')
    get_events('what is next month', get_calendar(write_file(get_ics_url('https://careers.unc.edu/calendar'), 'carolina_cal.ics')))

    #get_events('What is on 07/25/17?')

    # Stanford 
    #print d2
    #get_calendar(write_file(get_ics_url('https://events.stanford.edu/byCategory/28/'), 'stanford_cal.ics'))



    # Miami University
    
    #get_calendar(write_file(get_ics_url('http://miamioh.edu/emss/offices/career-services/events/index.html'), 'miami_cal.ics'))



    
    # University of Kansas
    
    #get_ics_url('https://calendar.ku.edu/')
    #get_calendar(write_file(get_ics_url('https://calendar.ku.edu/'), 'kansas_cal.ics'))


   
