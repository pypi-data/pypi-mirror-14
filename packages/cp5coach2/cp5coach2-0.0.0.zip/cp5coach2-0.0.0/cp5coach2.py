import os
import defcp5
os.chdir('C:\\Users\\liyl\\Desktop\\hfpy_ch6_data')
class AthleteList(list):
    def __init__(self,a_name,a_dob=None,a_times=[]):
        list.__init__([])
        self.name=a_name
        self.dob=a_dob
        self.extend(a_times)
    def top3(self):
        return(sorted(set([defcp5.sanitize(t) for t in self]))[0:3])
def get_coach_data(filename):
        try:
                with open(filename) as f:
                        data=f.readline()
                templ=data.strip().split(',')
                return(AthleteList(templ.pop(0),templ.pop(0),templ))
        except IOError as ioerr:
                print('File error: ' + str(ioerr))
                return(None)
