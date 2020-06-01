from django.shortcuts import render
from django.http import HttpResponse
from version2.extraction import *
from django.shortcuts import redirect
from version2.models import *
from django.views.decorators.cache import cache_control

import csv, random, datetime

num_search_results = 10
# algorithms to be initially displayed on the left and right, respectively
left_alg = "google"
right_alg = "altered"
# algorithms to be displayed on left and right after 10 turns
round_one_l = "google"
round_one_r = "altered"

# maps algorithm names to lists of snippets
alg_to_snippets = {
    left_alg: extractFromFile(round_one_l + ".txt", num_search_results),
    right_alg: extractFromFile(round_one_r + ".txt", num_search_results),
}

# whether or not to swap the left and right algorithms on a given turn
swap = [False, True, True, False, True, True, True, False, False, False, False, False, True, True, False, False, True, False, True, True, False]
# represents the order in which queries will actually appear
query_order = [6, 1, 16, 9, 7, 5, 17, 12, 2, 10, 19, 3, 8, 4, 20, 18, 15, 11, 13, 14] # randomly generated

def get_ip_address(request):
    """ use requestobject to fetch client machine's IP Address """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip
    
def consent(request):
    return render(request, 'version2/consent.html')
    
def demographics(request):
    if 'age' in request.GET:
        global respondent
        ip = get_ip_address(request)
        browser_info = request.user_agent.os.family + " " + request.user_agent.browser.family + " "
        if request.user_agent.is_pc:
            browser_info += "PC"
        else:
            browser_info += "Mobile"
            
        respondent = Respondent(
            age=request.GET['age'],
            gender=request.GET['gender'],
            education=request.GET['education'],
            ip_addr=ip,
            browser=browser_info)
        respondent.save()
        return redirect('version2-instructions', respondent_id=respondent.id)
    else:
        return render(request, 'version2/demographics.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def instructions(request, respondent_id):
    user = Respondent.objects.filter(id=respondent_id)[0]
    if user.curr_q != 0:
        return redirect('version2-redir', q_id=1, respondent_id=respondent_id)
    else:
        context = {
            'respondent_id': respondent_id
        }
        return render(request, 'version2/instructions.html', context)

def getAlgs(id):
    if id <= 20 and not swap[id-1]:
        left_alg = round_one_l
        right_alg = round_one_r
    else:
        left_alg = round_one_r
        right_alg = round_one_l
    
    return [left_alg, right_alg]

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def redir(request, q_id, respondent_id):
    user = Respondent.objects.filter(id=respondent_id)[0]
    id = user.curr_q
    
    if id < q_id:
        choice = 'NO_CHOICE'
        not_choice = 'NO_CHOICE'
        if 'radio' in request.GET:
            left_alg = getAlgs(id)[0]
            right_alg = getAlgs(id)[1]
            if request.GET['radio'] == 'left':
                choice = left_alg
                not_choice = right_alg
            else:
                choice = right_alg
                not_choice = left_alg
        
        if 'time_elapsed' in request.GET:
            response = Response(respondent=user,
                                query=Query.objects.filter(query_id=query_order[id-1])[0],
                                chosen_alg=Algorithm.objects.filter(name=choice)[0],
                                unchosen_alg=Algorithm.objects.filter(name=not_choice)[0],
                                time_elapsed=int(request.GET['time_elapsed']))
            response.save()
        
        id += 1
        user.curr_q = id 
        user.save()
    
    context = {
        'curr_qid': id,
        'respondent_id': respondent_id
    }
        
    return redirect('version2-home', q_id = id, respondent_id=respondent_id)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request, q_id, respondent_id):    
    user = Respondent.objects.filter(id=respondent_id)[0]
    
    if user.curr_q != q_id:
        return redirect('version2-redir', q_id=q_id, respondent_id=respondent_id)
        
    global left_alg
    global right_alg
        
    left_alg = getAlgs(q_id)[0]
    right_alg = getAlgs(q_id)[1]
    request.session.flush()
    if q_id <= 20:
        context = {
            'left_snippets': alg_to_snippets[left_alg][query_order[q_id-1]],
            'right_snippets': alg_to_snippets[right_alg][query_order[q_id-1]],
            'query_name': alg_to_snippets[right_alg][query_order[q_id-1]][0][0],
            'curr_qid': q_id + 1,
            'respondent_id': respondent_id
        }
        return render(request, 'version2/home.html', context)
    else:
        return redirect('version2-thanks', respondent_id=respondent_id)

def thanks(request, respondent_id):
    context = {
        'respondent_id': respondent_id
    }
    if 'mturk_id' in request.GET:
        resp = Respondent.objects.filter(id=respondent_id)[0]
        resp.mturk_id = request.GET['mturk_id']
        resp.save()
        return render(request, 'version2/code.html')
    else:
        return render(request, 'version2/thanks.html', context)

def exportUsers(request):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['mturk_id','age','gender','education','ip_addr','browser','date'])
    for u in Respondent.objects.all().values_list('mturk_id', 'age', 'gender', 'education', 'ip_addr', 'browser', 'date'):
        writer.writerow(u)
    today = datetime.date.today()
    filename = "users_" + today.strftime("%m_%d_%Y") + ".csv"
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response

def exportResponses(request):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['mturk_id','chosen','unchosen','query','num_fake_results','time_elapsed','date'])
    for r in Response.objects.all():
        writer.writerow([r.respondent.mturk_id, r.chosen_alg.name, r.unchosen_alg.name, r.query.query_name, r.query.num_fake, r.time_elapsed, r.date])
    today = datetime.date.today()
    filename = "responses_" + today.strftime("%m_%d_%Y") + ".csv"
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response