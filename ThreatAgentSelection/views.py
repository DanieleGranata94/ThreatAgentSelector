from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import TAReplies_Question, TAReplyCategory, Reply, ThreatAgentQuestion, TACategoryAttribute


@csrf_exempt
def homepage(request):
    return redirect('threat_agent_wizard')

@csrf_exempt
def threat_agent_wizard(request):
    context = {}
    # Generate question and related replies
    questions = ThreatAgentQuestion.objects.all()
    print(questions)
    questions_replies = TAReplies_Question.objects.all()
    questions_replies_list = []
    for question in questions:
        replies = []
        question_replies_dict = {}
        for reply in questions_replies:
            if question == reply.question:
                replies.append(reply.reply.reply)
        question_replies_dict['question'] = question.question
        question_replies_dict['replies'] = replies
        questions_replies_list.append(question_replies_dict)
    context['questions_replies'] = questions_replies_list

    return render(request, 'threat_agent_wizard.html', context)


@csrf_exempt
def threat_agent_generation(request):
    context = {}
    ThreatAgents = []
    ThreatAgentsPerAsset = []
    # for category in ThreatAgentCategory.objects.all():   #inizializzo la lista finale a tutti i TA
    # ThreatAgents.append(category)
    for reply in request.POST:  # per ogni risposta al questionario
        if (reply != 'csrfmiddlewaretoken'):
            ReplyObject = Reply.objects.filter(reply=reply).get()
            tareplycategories = TAReplyCategory.objects.filter(reply=ReplyObject)
            TAList = []
            for replycategory in tareplycategories.all():  # ogni categoria relativa ad una singola risposta
                # print(replycategory.reply.reply + " "+ replycategory.category.category)
                TAList.append(replycategory.category)
                question = TAReplies_Question.objects.filter(reply=ReplyObject)
            ThreatAgentsPerAsset.append((TAList, question))
    numQ3 = 0
    numQ4 = 0
    # conto il numero di risposte date per Q3 e Q4
    for ThreatAgentsList, question in ThreatAgentsPerAsset:  # per ogni risposta
        questionId = question.get().question.Qid
        if (questionId == "Q3"):
            numQ3 += 1
        if (questionId == "Q4"):
            numQ4 += 1

    i = 0
    j = 0
    ThreatAgentsListTemp = []
    for ThreatAgentsList, question in ThreatAgentsPerAsset:  # per ogni risposta
        questionId = question.get().question.Qid
        if (int(questionId) == 1):
            ThreatAgents = ThreatAgentsList
        if (int(questionId) == 2):
            ThreatAgents = intersection(ThreatAgents, ThreatAgentsList)
        if (int(questionId) == 3):
            if (i == 0):
                ThreatAgentsListTemp = ThreatAgentsList
            elif (i < numQ3):
                ThreatAgentsList = union(ThreatAgentsList, ThreatAgentsListTemp)
                ThreatAgentsListTemp = ThreatAgentsList
            if (i == numQ3 - 1):
                ThreatAgents = intersection(ThreatAgents, ThreatAgentsList)
            i = i + 1

        if (int(questionId) == 4):
            if (j == 0):
                ThreatAgentsListTemp = ThreatAgentsList
                j = j + 1
            elif (j == 1):
                ThreatAgentsListTemp = ThreatAgentsList
                j = j + 1
            elif (j < numQ4):
                ThreatAgentsList = union(ThreatAgentsList, ThreatAgentsListTemp)
                ThreatAgentsListTemp = ThreatAgentsList

    ThreatAgents = intersection(ThreatAgents, ThreatAgentsList)
    ThreatAgentsWithInfo = {}
    for ta in ThreatAgents:
        ThreatAgentsWithInfo[ta] = list(TACategoryAttribute.objects.filter(category=ta))
    context = {'ThreatAgents': ThreatAgentsWithInfo}
    return render(request, 'threat_agent_generation.html', context=context)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def union(lst1, lst2):
    lst3 = list(set(lst1 + lst2))
    return lst3

