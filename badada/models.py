# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Answer(models.Model):
    question_num = models.ForeignKey('Question', models.DO_NOTHING, db_column='question_num', blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answer'
        db_table_comment = '답변'


class AnswerMbtiScore(models.Model):
    id = models.OneToOneField(Answer, models.DO_NOTHING, db_column='id', primary_key=True)
    e = models.IntegerField(blank=True, null=True)
    i = models.IntegerField(blank=True, null=True)
    s = models.IntegerField(blank=True, null=True)
    n = models.IntegerField(blank=True, null=True)
    t = models.IntegerField(blank=True, null=True)
    f = models.IntegerField(blank=True, null=True)
    p = models.IntegerField(blank=True, null=True)
    j = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answer_mbti_score'
        db_table_comment = '답변별 MBTI 점수'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Beach(models.Model):
    beach = models.CharField(primary_key=True, max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    attribute_1 = models.CharField(max_length=1000, blank=True, null=True)
    attribute_2 = models.CharField(max_length=1000, blank=True, null=True)
    attribute_3 = models.CharField(max_length=1000, blank=True, null=True)
    recommendation_1 = models.CharField(max_length=1000, blank=True, null=True)
    recommendation_2 = models.CharField(max_length=1000, blank=True, null=True)
    recommendation_3 = models.CharField(max_length=1000, blank=True, null=True)
    category_1 = models.CharField(max_length=100, blank=True, null=True)
    category_2 = models.CharField(max_length=100, blank=True, null=True)
    category_3 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'beach'
        db_table_comment = '해변 정보'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Feedback(models.Model):
    good = models.IntegerField(blank=True, null=True)
    bad = models.IntegerField(blank=True, null=True)
    good_1 = models.IntegerField(blank=True, null=True)
    good_2 = models.IntegerField(blank=True, null=True)
    good_3 = models.IntegerField(blank=True, null=True)
    good_4 = models.IntegerField(blank=True, null=True)
    good_5 = models.IntegerField(blank=True, null=True)
    good_text = models.CharField(max_length=1000, blank=True, null=True)
    bad_1 = models.IntegerField(blank=True, null=True)
    bad_2 = models.IntegerField(blank=True, null=True)
    bad_3 = models.IntegerField(blank=True, null=True)
    bad_4 = models.IntegerField(blank=True, null=True)
    bad_5 = models.IntegerField(blank=True, null=True)
    bad_text = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'
        db_table_comment = '피드백'


class Mbti(models.Model):
    mbti = models.CharField(primary_key=True, max_length=4)
    beach = models.ForeignKey(Beach, models.DO_NOTHING, db_column='beach', blank=True, null=True)
    bad_mbti = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mbti'
        db_table_comment = 'mbti 관련 정보'


class MbtiCnt(models.Model):
    mbti = models.CharField(primary_key=True, max_length=5)
    mbti_cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mbti_cnt'
        db_table_comment = 'mbti별 누적 결과'


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question'
        db_table_comment = '질문'


class UserCnt(models.Model):
    total_user_cnt = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'user_cnt'
        db_table_comment = '서비스 사용자 수'
