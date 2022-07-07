from django.db import models


class ThreatAgentCategory(models.Model):
    category = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=500,null=True)
    common_actions = models.CharField(max_length=500,null=True)

class ThreatAgentQuestion(models.Model):
    Qid = models.CharField(max_length=500, null=True)
    question = models.CharField(max_length=500)

class ThreatAgentAttribute(models.Model):
    attribute = models.CharField(max_length=100,null=True)
    attribute_value = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=500,null=True)
    score = models.IntegerField(null=True)

class ThreatAgentQuestion(models.Model):
    Qid = models.CharField(max_length=500, null=True)
    question = models.CharField(max_length=500)

class Reply(models.Model):
    reply = models.CharField(max_length=500)
    multiple = models.BooleanField(default=False)

class TAReplies_Question(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE,null=True)
    question = models.ForeignKey(ThreatAgentQuestion, on_delete=models.CASCADE,null=True)

class TACategoryAttribute(models.Model):
    category = models.ForeignKey(ThreatAgentCategory, on_delete=models.CASCADE, null=True)
    attribute = models.ForeignKey(ThreatAgentAttribute, on_delete=models.CASCADE, null=True)

class TAReplyCategory(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(ThreatAgentCategory, on_delete=models.CASCADE, null=True)
