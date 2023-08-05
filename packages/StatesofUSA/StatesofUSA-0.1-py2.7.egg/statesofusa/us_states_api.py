#!/usr/bin/env python

__author__ = 'Isham'

from constants import *
import csv
from rest_base import RESTBase


class USStates(RESTBase):
    """
        Flask API for getting states of USA.
        Post parameters :
            page : the page number
            items_per_page : Number of states in the page.
            
        Returns JSON data of the States for the requested page.
        Also returns metadata on the requested and available pages.
    """
    def __init__(self, *args, **kwargs):
        self.json_input_dict = {}
        super(USStates, self).__init__(*args, **kwargs)

    def validate_post_parameters(self, request):
        self.json_input_dict = request.form
        error_found = False
        
        # Validating the post parameters
        try:
            page_num = int(self.json_input_dict[KEY_ITEMS_PER_PAGE])
        except KeyError:
            error_found = True
            error_message = "{0} is a mandatory argument, not passed.".format(KEY_ITEMS_PER_PAGE)
        except ValueError:
            error_found = True
            error_message = "Invalid value found for {0}".format(KEY_ITEMS_PER_PAGE)
            
        try:
            states_per_page = int(self.json_input_dict[KEY_PAGE_NUM])
        except KeyError:
            error_found = True
            error_message = "{0} is a mandatory argument, not passed.".format(KEY_PAGE_NUM)
        except ValueError:
            error_found = True
            error_message = "Invalid value found for {0}".format(KEY_PAGE_NUM)

        if error_found :
            validation_type = ValidationTypes.VALIDATION
            return Status.FAILURE, validation_type, error_message
        else:
            return (Status.SUCCESS, None, None)

    def process_post(self, *args, **kwargs):
        page_num = int(self.json_input_dict[KEY_PAGE_NUM])
        states_per_page = int(self.json_input_dict[KEY_ITEMS_PER_PAGE])
        # Using the rsutl template
        result_data_dict = API_RESULT_DATA_TEMPLATE
        
        states_dict = {}
        
        # The first page starts from 0th line
        start_point = (page_num - 1) * states_per_page + 1
        end_point = start_point + states_per_page
        with open('states.csv', 'r') as csv_states:
            csv_reader = csv.reader(csv_states, delimiter = ',', quotechar = '"')
            next(csv_reader, None)  # skip the headers
            
            for item in csv_reader:
                (count, state, abbv) = item
                count = int(count)
                
                if count < start_point or count >= end_point:
                    continue
                states_dict[state] = abbv
        
        available_pages = count / states_per_page
        # If states_per_page/count return a remainder, there are states remaining.
        if count % states_per_page:
            available_pages += 1
        
        if page_num > available_pages:
            message = "Page number not Found."
        else:
            message = "States of the U.S.A"
        
        result_data_dict['result'] = states_dict
        # Constructing meta data.
        result_data_dict['meta'][KEY_PAGE_NUM] = page_num
        result_data_dict['meta'][KEY_ITEMS_PER_PAGE] = states_per_page
        result_data_dict['meta'][KEY_AVAILABLE_PAGES] = available_pages
    
        return (Status.SUCCESS, ValidationTypes.NONE, message, result_data_dict)
    

