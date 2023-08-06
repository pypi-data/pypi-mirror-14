import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

#use oauth 1.5.2
class GoogleSheetParser(object):
    def __init__(self, driveCredentials, sheetId, workSheetName, cellFilter = None):
        self.driveCredentials = driveCredentials
        self.sheetId = sheetId
        self.workSheetName = workSheetName
        self.cellFilter = cellFilter

        self.allRows = []

    def fetchRows(self):
        json_key = json.load(open(self.driveCredentials))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
        gc = gspread.authorize(credentials)
        wks = gc.open_by_key(self.sheetId).worksheet(self.workSheetName)

        self.allRows = wks.get_all_values()
        return self.allRows

    def filterRows(self, cellFilter):
        filteredRows = []
        if not cellFilter:
            return self.allRows

        for row in self.allRows:
            for cell in row:
                    if cellFilter(cell):
                        filteredRows.append(row)
        return filteredRows

    def run(self):
        self.fetchRows()
        return self.filterRows(self.cellFilter)
