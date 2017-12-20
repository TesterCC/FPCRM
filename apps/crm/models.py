#!/usr/bin/env python
# coding=utf-8

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    """
    客户信息表
    """
    name = models.CharField(max_length=32, blank=True, null=True)
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    # tuple
    source_choices = ((0, '转介绍'),
                      (1, 'QQ群'),
                      (2, '官网'),
                      (3, 'SEM'),
                      (4, 'IT社区'),
                      (5, '知乎'),
                      (6, '市场推广'))
    source = models.SmallIntegerField(choices=source_choices)
    # 转介绍人信息
    referral_from = models.CharField(verbose_name="转介绍人QQ", max_length=64, blank=True, null=True)
    consult_course = models.ForeignKey("Course", verbose_name="咨询课程")
    content = models.TextField(verbose_name="咨询详情")
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    tags = models.ManyToManyField("Tag", blank=True)

    status_choices = ((0, '已报名'),
                      (1, '未报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=1)

    memo = models.TextField(verbose_name="课程备注", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "客户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.qq


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=32)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CustomerFollowUp(models.Model):
    """
    客户跟进表
    """
    customer = models.ForeignKey("Customer", verbose_name="跟进客户名")
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    date = models.DateTimeField(auto_now_add=True)
    intention_choices = ((0, '2周内报名'),
                         (1, '1个月内报名'),
                         (2, '近期无报名计划'),
                         (3, '已在其它机构报名'),
                         (4, '已报名'),
                         (5, '已拉黑'),
                        )
    intention = models.SmallIntegerField(choices=intention_choices)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "客户跟进"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<%s : %s>" % (self.customer.qq, self.intention)


class Course(models.Model):
    """
    课程表
    """
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()     # 正数
    period = models.PositiveSmallIntegerField(verbose_name="周期（月）")
    outline = models.TextField()

    class Meta:
        verbose_name = "课程表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Branch(models.Model):
    """
    校区
    """
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=128)

    class Meta:
        verbose_name = "分支机构"
        verbose_name_plural = verbose_name


class CourseRecord(models.Model):
    """
    上课记录
    """
    from_class = models.ForeignKey("ClassList", verbose_name="班级")
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节(天)")
    teacher = models.ForeignKey("UserProfile")
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "上课记录"
        verbose_name_plural = verbose_name
        unique_together = ("from_class", "day_num")

    def __str__(self):
        return "%s %s" % (self.from_class, self.day_num)


class ClassList(models.Model):
    """
    班级表
    """
    branch = models.ForeignKey("Branch", verbose_name="校区")
    course = models.ForeignKey("Course")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teacher = models.ManyToManyField("UserProfile")
    class_type_choices = ((0, '面授（脱产）'),
                          (1, '面授（周末）'),
                          (2, '网络班'))
    class_type = models.SmallIntegerField(choices=class_type_choices, verbose_name="班级类型")
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="结业日期", blank=True, null=True)

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = verbose_name
        unique_together = ('branch', 'course', 'semester')     # 联合唯一

    def __str__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)


class StudyRecord(models.Model):
    """
    学习记录
    """
    student = models.ForeignKey("Enrollment")
    course_record = models.ForeignKey("CourseRecord")
    attendance_choices = ((0, '已签到'),
                          (1, '迟到'),
                          (2, '缺勤'),
                          (3, '早退'))
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0)
    score_choices = ((100, "A+"),
                     (90, "A"),
                     (85, "B+"),
                     (80, "B"),
                     (75, "B-"),
                     (70, "C+"),
                     (60, "C"),
                     (40, "C-"),
                     (-50, "D"),
                     (-100, "COPY"),
                     (0, "N/A"),   # Not Available
                     )
    score = models.SmallIntegerField(choices=score_choices)
    memo = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "学习记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s %s" % (self.student, self.course_record, self.score)


class Enrollment(models.Model):
    """
    报名表
    """
    customer = models.ForeignKey("Customer")
    enrolled_class = models.ForeignKey("ClassList", verbose_name="所报班级")
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    contract_agreed = models.BooleanField(default=False, verbose_name="学员已同意合同条款")
    contract_approved = models.BooleanField(default=False, verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "报名"
        verbose_name_plural = verbose_name
        unique_together = ("customer", "enrolled_class")


class Payment(models.Model):
    """
    缴费记录
    """
    customer = models.ForeignKey("Customer")      # 先缴费，才能报名
    course = models.ForeignKey("Course", verbose_name="所报课程")
    amount = models.PositiveIntegerField(verbose_name="数额", default=500)
    consultant = models.ForeignKey("UserProfile")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "缴费记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s" % (self.customer, self.amount)


class UserProfile(models.Model):
    """
    账号表
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role", blank=True)

    class Meta:
        verbose_name = "账号表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Role(models.Model):
    """ 
    角色表
    """
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField("Menu", blank=True)    # null=True is not useful for ManyToMany

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    侧边菜单
    """
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



