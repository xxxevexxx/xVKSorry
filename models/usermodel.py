import time
from tortoise import Model, fields


class Users(Model):
    id = fields.IntField(pk=True)
    user = fields.BigIntField()
    owner = fields.BigIntField()
    nick = fields.TextField(max_length=255, default="NoName")
    rank = fields.IntField(max_length=1, default=1)
    token = fields.TextField(max_length=255, default="None")
    balance = fields.IntField(max_length=6, default=0)
    register = fields.IntField(max_length=11, default=time.time())
    chats_list = fields.JSONField(default=list)
    ignore_list = fields.JSONField(default=list)
    trusted_list = fields.JSONField(default=list)
    dialogue_list = fields.JSONField(default=list)
    prefix_commands = fields.TextField(max_length=255, default="..")
    prefix_scripts = fields.TextField(max_length=255, default=",,")
    prefix_repeats = fields.TextField(max_length=255, default="#")
    message_time = fields.DatetimeField(auto_now_add=True)
    command_time = fields.DatetimeField(auto_now_add=True)
    scripts = fields.ReverseRelation["Scripts"]
    aliases = fields.ReverseRelation["Aliases"]
    triggers = fields.ReverseRelation["Triggers"]
    templates = fields.ReverseRelation["Templates"]


class Scripts(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="scripts")
    stats_li = fields.IntField(max_length=99, default=0)
    stats_dr = fields.IntField(max_length=99, default=0)
    stats_uv = fields.IntField(max_length=99, default=0)
    stats_ot = fields.IntField(max_length=99, default=0)
    stats_cl = fields.IntField(max_length=99, default=0)
    stats_ar = fields.IntField(max_length=99, default=0)
    condition_li = fields.BooleanField(default=False)
    condition_dr = fields.BooleanField(default=False)
    condition_uv = fields.BooleanField(default=False)
    condition_ot = fields.BooleanField(default=False)
    condition_cl = fields.BooleanField(default=False)
    condition_ar = fields.BooleanField(default=False)


class Aliases(Model):
    user = fields.ForeignKeyField("models.Users", related_name="aliases")
    name = fields.TextField(max_length=4096)
    command = fields.TextField(max_length=4096)


class Triggers(Model):
    user = fields.ForeignKeyField("models.Users", related_name="triggers")
    name = fields.TextField(max_length=4096)
    trigger = fields.JSONField(default=list)
    command = fields.TextField(max_length=4096)


class Templates(Model):
    user = fields.ForeignKeyField("models.Users", related_name="templates")
    name = fields.TextField(max_length=4096)
    media = fields.BooleanField(default=False)
    message_id = fields.IntField(max_length=255)