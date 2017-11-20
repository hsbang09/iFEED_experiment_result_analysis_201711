import csv
import numpy as np
import pandas as pd

NETID_COLUMN = 18 - 1
KEY_NUM_COLUMN = 164 - 1

TARGET_REGION_ORDER_SETUP = 19 - 1
FIRST_TASK_START = 20 - 1
FIRST_TASK_END = 45 - 1
SECOND_TASK_START = 92 - 1
SECOND_TASK_END = 117 - 1

FIRST_TLX_START = 45 - 1
FIRST_TLX_END = 66 - 1
FIRST_UEQ_START = 66 - 1
FIRST_UEQ_END = 92 - 1
SECOND_TLX_START = 117 - 1
SECOND_TLX_END = 138 - 1
SECOND_UEQ_START = 138 - 1
SECOND_UEQ_END = 164 - 1

AGE = 165 - 1
GENDER = 166 - 1
MAJOR = 168 - 1
PRIOR_EXPERIENCE = 169 - 1

LOW_COST_LOW_PERF_ANSWER = [0,0,0,1,0,0,1,1,1,0,0,1,0,1,1,0,0,0,0,1,1,0,1,0,1]
HIGH_COST_HIGH_PERF_ANSWER = [1,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1,0,1,0,0,0]

SUBJECTS_TO_SKIP_NETID = ['wdl32','sv457','ad629','jh2524','cw828','heh56','hhh57','sf373','ccm254'] 
SUBJECTS_TO_SKIP_KEYNUM = ['321321','9328687356','7827461360','8392086791','9988798887','670229880','7768461265','Not given','8506366701']

SUBJECTS_TAKING_SYSEN5400 = [
    '123123123',
    '2620672040', 
    '3137288120',
    '9191698327',
    '5371946331',
    '69776412',
    '9098178254',
    '9258315966',
    '6565205741',
    '1275213599',
    '9826509423',
    '4022934325',
    '8013804199',
]

CONDITION_ASSIGNMENTS = {
    '123123123':0,  # Jamil SYSEN5400
    '4340870324':0, # Kevin
    'atf39':0, # Lexie
    'lm573':1, # Liza    
    '3306569930': 0, # Megan
    '4334445073': 0, # Seongha
    '64402823': 1, # Hadley
    '3137288120': 1, # Kyle SYSEN5400
    '2620672040': 0, # Gregory SYSEN5400
    '2133534586': 1, # Lucy
    '9191698327': 0, # Justin SYSEN5400
    'yk724': 1, # Yeonui
    '5371946331': 0, # Brian SYSEN5400
    '9098178254': 0, # Megan SYSEN5400
    '69776412': 0, # Alex SYSEN5400
    '8500084894': 0, # Suwon
    '3875682746': 1, # Jiyoon
    '9258315966': 0, # Miteshkumar SYSEN5400
    '1951642000': 0, # Iris
    '6565205741': 1, # Yuval SYSEN5400
    '6065280933': 1, # Eric
    'kd439': 0, # Kaustav
    '1275213599': 1, # Benjamin SYSEN5400
    '2521704359': 1, # Stephanie
    '9645975744': 0, # Larry
    '9031693318': 0, # Eric
    '3514699334': 1, # Byungdoo
    '9826509423': 0, # Dante SYSEN5400
    'lsc94': 1, # Lauren
    '4022934325': 0, # Harley SYSEN5400
    '8013804199': 1, # Daewoon SYSEN5400
}


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


class ResultAnalyzer():
    
    def __init__(self):
        
        self.first_condition_scores = []
        self.second_condition_scores = []
        
        self.results = []
    
    def readData(self,csvFile="/Users/bang/workspace/iFEED-experiment-201711-result/result/20171120.csv"):
        with open(csvFile, newline='') as file:
            content = csv.reader(file, delimiter=',')
            for i, row in enumerate(content):
                if i<3: # Skip header info
                    continue
                else:
                    index = i-3

                    netid = row[NETID_COLUMN]
                    keyNum = row[KEY_NUM_COLUMN]
                    
                    # Task information
                    firstTaskAnswer = row[FIRST_TASK_START:FIRST_TASK_END]
                    secondTaskAnswer = row[SECOND_TASK_START:SECOND_TASK_END]
                    targetRegionOrder = row[TARGET_REGION_ORDER_SETUP]
                    
                    # TLX
                    firstTLX = row[FIRST_TLX_START:FIRST_TLX_END]
                    secondTLX = row[SECOND_TLX_START:SECOND_TLX_END]
                    
                    # UEQ
                    fistUEQ = row[FIRST_UEQ_START:FIRST_UEQ_END]
                    secondUEQ = row[SECOND_UEQ_START:SECOND_UEQ_END]                    
                    
                    # Demographic infomration
                    age = row[AGE]
                    gender = row[GENDER]
                    major = row[MAJOR]
                    prior_experience = row[PRIOR_EXPERIENCE]
                    
                    # Create subject instance
                    s = Subject(netid,keyNum)
                    
                    # Skip subjects with invalid procedure
                    skip = False
                    for identifier in SUBJECTS_TO_SKIP_NETID:
                        if s.identify(identifier):
                            skip = True
                            break
                     
                    if not skip:
                        for identifier in SUBJECTS_TO_SKIP_KEYNUM:
                            if s.identify(identifier):
                                skip = True
                                break
                    if skip:
                        continue
                    else:
                        identified = False
                        for key in CONDITION_ASSIGNMENTS:
                            if s.identify(key):
                                identified=True
                                s.setConditionOrder(CONDITION_ASSIGNMENTS[key])
                                break
                        
                        if not identified:
                            raise ValueError('Unidentified Subject: {0}'.format(identifier))
                        
                    # Check for students taking SYSEN5400
                    for key in SUBJECTS_TAKING_SYSEN5400:
                        if s.identify(key):
                            s.setSYSEN5400()
                        
                    s.setTargetRegionOrder(targetRegionOrder)
                    s.gradeTask(0, firstTaskAnswer)
                    s.gradeTask(1, secondTaskAnswer)  
                    #s.setTLX(0, firstTLX)
                    #s.setTLX(1, secondTLX)
                    s.setDemographicInfo(age,gender,major,prior_experience)
                    self.results.append(s)
                    
                    print(s.toString())
            
            print('Total {0} subject data added out of {1}'.format(len(self.results), index+1 ))
            
    def getSTEMMajors(self, subjects):
        out = []
        for subj in subjects:
            if subj.major == "13": # Non-STEM    
                pass
            else:
                out.append(subj)  
        return out
    
    def getSubjectsWithPriorExperience(self, subjects):
        out = []
        for subj in subjects:
            if subj.prior_experience == "1": # Has-prior-experience  
                out.append(subj)  
        return out
    
    def getSubjectsTakingSYSEN5400(self, subjects):
        out = []
        for subj in subjects:
            if subj.SYSEN5400 : # Has-prior-experience  
                out.append(subj)  
        return out
                
    def filterByDemographics(self, STEM=False, NonSTEM=False, prior_experience=False, SYSEN5400 = False, NoSYSEN5400 = False):
        out = self.results
        if STEM:
            out = self.getSTEMMajors(out)
        if NonSTEM:
            stem = self.getSTEMMajors(out)
            out = []
            for subj in self.results:
                if subj not in stem:
                    out.append(subj)            
        if prior_experience:
            out = self.getSubjectsWithPriorExperience(out)
        if SYSEN5400:
            out = self.getSubjectsTakingSYSEN5400(out)
        if NoSYSEN5400:
            sysen5400 = self.getSubjectsTakingSYSEN5400(out)
            out = []
            for subj in self.results:
                if subj not in sysen5400:
                    out.append(subj)
        return out
    
    def getScoreData(self, subjects, condition_effect=True, order_effect=False, returnDataFrame = False, colnames = None):   
        
        first_scores = []
        second_scores = []        
        
        if order_effect:
            for subj in subjects:
                first_scores.append(subj.first_task_score)
                second_scores.append(subj.second_task_score)
        else:
            for subj in subjects:
                first_scores.append(subj.first_condition_score)
                second_scores.append(subj.second_condition_score)
                
        if returnDataFrame is False:
            return first_scores, second_scores
        else:
            scores = np.array([first_scores,second_scores])
            scores = np.transpose(scores)
            scores = pd.DataFrame(scores, columns = colnames)
            return scores
                
    def printStatistics(self, subjects, condition_effect=True, order_effect=False):
        
        first_scores, second_scores = self.getScoreData(subjects, condition_effect, order_effect)
        
        first_mean = np.mean(first_scores)
        second_mean = np.mean(second_scores)
        first_std = np.std(first_scores)
        second_std = np.std(second_scores)
        
        if order_effect:    
            print("First Task Score Mean: {0}, Second Task Score Mean: {1}".format(first_mean, second_mean))
            print("First Task Score Stdev: {0}, Second Task Score Stdev: {1}".format(first_std, second_std))
        else:
            print("First Condition Score Mean: {0}, Second Condition Score Mean: {1}".format(first_mean, second_mean))
            print("First Condition Score Stdev: {0}, Second Condition Score Stdev: {1}".format(first_std, second_std))  
            
        return first_mean, second_mean, first_std, second_std
            
                
class Subject():
    
    def __init__(self, netID=None, keyNum=None):
        if netID == "":
            netID = None
        if keyNum == "":
            keyNum = None
            
        self.netID = netID
        
        if keyNum is None:
            self.keyNum = None
        elif isinstance(keyNum, str): 
            self.keyNum = keyNum
        else: # Save it as string
            self.keyNum = str(keyNum)
            
        self.condition_order = None
        self.target_region_order = None
        
        self.first_task_result = None
        self.second_task_result = None
        self.first_task_score = None
        self.second_task_score = None
        
        self.first_condition_result = None
        self.second_condition_result = None
        self.first_condition_score = None
        self.second_condition_score = None
        
        self.first_TLX = None
        self.second_TLX = None
        
        self.SYSEN5400 = False
        
        
    def toString(self):
        #out = "netID: {0}, keyNum: {1}, First task score: {2}, Second task score: {3}, First TLX: {4:.2f}, Second TLX: {5:.2f}".format(self.netID,self.keyNum, int(sum(self.first_task_result)/25*100), int(sum(self.second_task_result)/25*100), self.first_TLX, self.second_TLX)
        if self.condition_order is not None:
            out = "netID: {0}, keyNum: {1}, First condition score: {2}, Second condition score: {3}".format(self.netID,self.keyNum, self.first_condition_score, self.second_condition_score)        
        else:
            out = "netID: {0}, keyNum: {1}, First task score: {2}, Second task score: {3}".format(self.netID,self.keyNum, self.first_task_score, self.second_task_score)    
            
        return out
        
    def setDemographicInfo(self, age,gender,major,prior_experience):
        self.age = age
        self.gender = gender
        self.major = major
        self.prior_experience = prior_experience
        
    def setSYSEN5400(self):
        self.SYSEN5400 = True
    
    def identify(self, identifier): # identifier must be string
        if self.netID == identifier:
            return True
        elif self.keyNum == identifier:
            return True
        else:
            return False
    
    def setTargetRegionOrder(self, n):
        if n==1: # Lower-cost-lower-performance region first
            self.target_region_order = [0, 1]
        else: # n=2: Higher-cost-higher-performance region first
            self.target_region_order = [1, 0]
            
    def setConditionOrder(self, n):
        if n==0: # Design space exploration first
            self.condition_order = [0, 1]
        else: # Feature space exploration first
            self.condition_order = [1, 0]
    
    def gradeTask(self, n, answers):
        if n==0: # First task
            target_region = self.target_region_order[0]
        else: # Second task
            target_region = self.target_region_order[1]
        
        if target_region == 0: # Low-cost-low-performance
            correctAnswers = LOW_COST_LOW_PERF_ANSWER
        else:
            correctAnswers = HIGH_COST_HIGH_PERF_ANSWER
        
        graded = [False] * len(correctAnswers)
        
        for i in range(len(correctAnswers)):
            userAnswer = answers[i]
            correctAnswer = correctAnswers[i]
            if userAnswer is None or userAnswer == "":
                pass # Count as a wrong answer
            else:
                if userAnswer == "2":
                    userAnswer = "0"
                if correctAnswer == int(userAnswer):
                    graded[i] = True
        
        if n==0: # First task
            self.first_task_result = graded
            #self.first_task_score = int(sum(graded)/25*100)
            self.first_task_score = sum(graded)
            if self.condition_order is not None:
                if self.condition_order[0] == 0:
                    self.first_condition_result = graded
                    self.first_condition_score = self.first_task_score
                else:
                    self.second_condition_result = graded
                    self.second_condition_score = self.first_task_score
            
        else: # Second task
            self.second_task_result = graded
            #self.second_task_score = int(sum(graded)/25*100)
            self.second_task_score = sum(graded)
            if self.condition_order is not None:
                if self.condition_order[0] == 0:
                    self.second_condition_result = graded
                    self.second_condition_score = self.second_task_score
                else:
                    self.first_condition_result = graded            
                    self.first_condition_score = self.second_task_score
            
    def setTLX(self, n, TLXAnswers): 
        if n==0: # First task
            self.first_TLX = self.getTLX_weighted(TLXAnswers)
        else: # Second task
            self.second_TLX = self.getTLX_weighted(TLXAnswers)        
    
    def getTLX(self, TLXAnswers):
        scores = TLXAnswers[0:6]
        scores = [int(d) if d is not '' else 0 for d in scores]        
        return np.mean(scores)
        # mental, physical, temporal, performance, effort, frustration
    
    def getTLX_weighted(self, TLXAnswers, returnIndividualLoads = False):
        scores = TLXAnswers[0:6]
        scores = [int(d) if d is not '' else 0 for d in scores] 
        unweightedTLX = {"mental":scores[0],"physical":scores[1],"temporal":scores[2],"performance":scores[3],"effort":scores[4],"frustration":scores[5]}
        
        data = TLXAnswers[6:]
        data = [int(d) for d in data]
        weights = {"mental":0,"physical":0,"temporal":0,"performance":0,"effort":0,"frustration":0}
        
        if data[0] == 1:
            weights['effort'] += 1
        else:
            weights['performance'] += 1
        
        if data[1] == 1:
            weights['temporal'] += 1
        else:
            weights['frustration'] += 1
        
        if data[2] == 1:
            weights['temporal'] += 1
        else:
            weights['effort'] += 1
            
        if data[3] == 1:
            weights['physical'] += 1
        else:
            weights['frustration'] += 1
            
        if data[4] == 1:
            weights['performance'] += 1
        else:
            weights['frustration'] += 1
        
        if data[5] == 1:
            weights['physical'] += 1
        else:
            weights['temporal'] += 1
            
        if data[6] == 1:
            weights['physical'] += 1
        else:
            weights['performance'] += 1
            
        if data[7] == 1:
            weights['temporal'] += 1
        else:
            weights['mental'] += 1
        
        if data[8] == 1:
            weights['frustration'] += 1
        else:
            weights['effort'] += 1
            
        if data[9] == 1:
            weights['performance'] += 1
        else:
            weights['mental'] += 1
            
        if data[10] == 1:
            weights['performance'] += 1
        else:
            weights['temporal'] += 1
            
        if data[11] == 1:
            weights['mental'] += 1
        else:
            weights['effort'] += 1
            
        if data[12] == 1:
            weights['mental'] += 1
        else:
            weights['physical'] += 1
            
        if data[13] == 1:
            weights['effort'] += 1
        else:
            weights['physical'] += 1
            
        if data[14] == 1:
            weights['frustration'] += 1
        else:
            weights['mental'] += 1          
        
        try:
        
            weightedTLX = {}
            for key in weights:
                weights[key] = weights[key]/15
                weightedTLX[key] = weights[key] * unweightedTLX[key]
        
        except TypeError as e:
            print(unweightedTLX[key])
            raise ValueError("asdfa")
        
        if returnIndividualLoads:
            return weightedTLX
        else:
            values = []
            for key in weightedTLX:
                values.append(weightedTLX[key])
            
            return np.mean(values)
            
            
            
if __name__=='__main__':
    analyzer = ResultAnalyzer()
    
    analyzer.readData()
    analyzer.printStatistics()