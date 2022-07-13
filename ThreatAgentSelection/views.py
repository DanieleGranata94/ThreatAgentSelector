from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import TAReplies_Question, TAReplyCategory, Reply, ThreatAgentQuestion, TACategoryAttribute, \
    ThreatAgentCategory


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
    motive=0
    opportunity=0
    size=0
    skill=0
    for ta in ThreatAgents:
        ThreatAgentsWithInfo[ta.category]={}
        ThreatAgentsWithInfo[ta.category]['attributes'] = list(TACategoryAttribute.objects.filter(category=ta))
        motive,opportunity,size,skill=calculate_threat_agent_risks(ta)
        ThreatAgentsWithInfo[ta.category]['motive']=motive
        ThreatAgentsWithInfo[ta.category]['opportunity']=opportunity
        ThreatAgentsWithInfo[ta.category]['size']=size
        ThreatAgentsWithInfo[ta.category]['skill']=skill
        ThreatAgentsWithInfo[ta.category]['description']=ta.description
        ThreatAgentsWithInfo[ta.category]['common_actions']=ta.common_actions
    print(ThreatAgentsWithInfo)
    context = {'ThreatAgents': ThreatAgentsWithInfo}
    return render(request, 'threat_agent_generation.html', context=context)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def union(lst1, lst2):
    lst3 = list(set(lst1 + lst2))
    return lst3


def calculate_threat_agent_risks(ThreatAgent):
    category=ThreatAgent.category
    TACategory = ThreatAgentCategory.objects.get(category=category)
    # per ogni categoria ottieni i Attribute relativi e calcola i 4 parametri owasp con le formule nella tesi.
    TACategoryAttributes = TACategoryAttribute.objects.filter(category=TACategory)
    limits = 0
    intent = 0
    access = 0
    resources = 0
    visibility = 0
    skills = 0

    # scorro gli attributi di category
    for TACategoryAttributeVar in TACategoryAttributes:
        if (TACategoryAttributeVar.attribute.attribute == 'Skills'):
            skills = TACategoryAttributeVar.attribute.score
        if (TACategoryAttributeVar.attribute.attribute == 'Resources'):
            resources = TACategoryAttributeVar.attribute.score
        if (TACategoryAttributeVar.attribute.attribute == 'Visibility'):
            visibility = TACategoryAttributeVar.attribute.score
        if (TACategoryAttributeVar.attribute.attribute == 'Limits'):
            limits = TACategoryAttributeVar.attribute.score
        if (TACategoryAttributeVar.attribute.attribute == 'Intent'):
            intent = TACategoryAttributeVar.attribute.score
        if (TACategoryAttributeVar.attribute.attribute == 'Access'):
            access = TACategoryAttributeVar.attribute.score

    OWASP_Motive = int(((((intent / 2) + (limits / 4)) / 2) * 10))
    OWASP_Opportunity = int(((((access / 2) + (resources / 6) + (visibility / 4)) / 3) * 10))
    OWASP_Size = int((resources / 6) * 10)
    OWASP_Skill = int((skills / 4) * 10)
    return OWASP_Motive,OWASP_Opportunity,OWASP_Size,OWASP_Skill



