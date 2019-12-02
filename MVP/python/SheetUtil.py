'''
Wrapper for the Google Sheets functions
Handles low level management of the sheet
Author: Howard Webb
Date: 11/22/2019
'''

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from LogUtil import Logger

# If modifying these scopes, delete the file token.pickle.

CRED = '/home/pi/MVP/python/credentials.json'

class SheetUtil(object):

    def __init__(self, sheet_name, scope, logger=None):
        if logger == None:
            self._logger = Logger("SheetUtil", Logger.DETAIL)
        else:
            self._logger = logger
        self._logger.debug("Initialize SheetUtil")
        self._sheet_name = sheet_name
        self._scope = scope

        # The ID and range of a sample spreadsheet.
        self._sheet = self.open_sheet()
        self._logger.debug("%s: %s" % ('Opened', sheet_name))
        

    def open_sheet(self):
        '''
        Args:
            self
        Returns:
            sheet - sheet service
        Throws:
            None

        '''
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CRED, self._scope)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        return sheet
        
    def getData(self, range_name):        
        '''
        Read data range from a sheet
        Args:
            self
            range: where to get data from, includes tab
        Returns:
            values: data from sheet
        Throws:
            None

        '''
        result = self._sheet.values().get(spreadsheetId=self._sheet_name,
            range=range_name).execute()
        values = result.get('values', [])
        return values

                
    def append(self, range_name, values):
        '''
        Append data to a range
        Args:
            self
            range_name - where to put the data
            values - what to add
        Returns:
            None
        Throws:
            None

        '''
                
        # Append Test
        resource = {"majorDimension": "COLUMNS", "values": values}

        result = self._sheet.values().append(spreadsheetId=self._sheet_name,
                                    range=range_name, body = resource, valueInputOption="USER_ENTERED").execute()            

   
def test(level=Logger.DEBUG):
    SAMPLE_RANGE_NAME = 'Fairchild!A2:E'
    sheet_name = '1Mtlr_-yqwdEwXFEcaLoEP01aDN7vvOosDOEerFpDkaI'
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    #APPEND_RANGE = 'Phenotype!A1'    
    sheet = SheetUtil(sheet_name, scope)
    sheet._logger.setLevel(level)  
    values = sheet.getData(SAMPLE_RANGE_NAME)
    if not values:
        sheet._logger.debug('No data returned')
    else:
        sheet._logger.debug('Name, Major')        
        for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
            sheet._logger.debug('%s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[3], row[4]))        
        # Append Test            
    append_range = "Phenotype!A1";
    values = [['testone'],['testtwo'],['testthree'],['testfour'],['testfive'],['testsix']]
    
    sheet.append(append_range, values)            
    

if __name__ == '__main__':
    test()