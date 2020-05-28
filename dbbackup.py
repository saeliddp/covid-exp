from version2.models import *
responses = Response.objects.all()
users = Respondent.objects.all()

def toCSV(data):
    out = ""
    out += str(data[0])
    for d in data[1:]:
        out += "," + str(d)
    return out

def printResponses(start_ind=0, end_ind=len(responses)-1):
    print("mturk_id,chosen,unchosen,query,num_fake_results,time_elapsed,date")
    for r in responses:
        print(toCSV([r.respondent.mturk_id, r.chosen_alg.name, r.unchosen_alg.name, r.query.query_name, r.query.num_fake, r.time_elapsed, r.date]))
        
def printUsers(start_ind=0, end_ind=len(users)-1):
    print("mturk_id,age,gender,education,ip_addr,browser,date")
    for u in users:
        print(toCSV([u.mturk_id, u.age, u.gender, u.education, u.ip_addr, u.browser, u.date]))