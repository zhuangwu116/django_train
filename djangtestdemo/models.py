# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
import datetime
# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline

class ArticleCategoryManager(models.Manager):
    def premenu(self,types):
        objects=self.filter(types=types,isvalid=False)
        q=None
        if len(objects)>0:
            q=~Q(path_id__startswith=objects[0].path_id)
            for i in range(1,len(objects)):
                q=q|~Q(path_id__startswith=objects[i].path_id)
        if q:
            objects=self.filter(types=types).filter(q)
        else:
            objects=self.filter(types=types)
        return objects
        # 管理平台获取的菜单
    def menu(self):
        menulists = []
        objects = self.all()
        i = 0
        for obj in objects:
            path_count = len(obj.path.split(':'))
            menudirc={}
            menudirc['id']=obj.id
            menudirc['name']=obj.name
            menudirc['parent']=obj.parent
            menudirc['path']=obj.path
            menudirc['serialnumber']=obj.serialnumber
            menudirc['isvalid']=obj.isvalid
            menudirc['path_id']=obj.path_id
            menudirc['types']=obj.types
            menudirc['link']=obj.link
            menudirc['date']=obj.date
            i += 1
            if i < len(objects):
                back_path_count = len(objects[i].path.split(':'))
                if path_count > back_path_count:
                   menudirc['html']='<div style="text-indent:%spx;">|__%s</div>' % (path_count * 25, obj.name)
                else:
                    if path_count == 1:
                         menudirc['html']='<div style="text-indent:%spx;">%s</div>' % (path_count * 25, obj.name)
                    else:
                        menudirc['html'] ='<div style="text-indent:%spx;">|--%s</div>' % (path_count * 25, obj.name)
            else:
                if path_count == 1:
                    menudirc['html'] ='<div style="text-indent:%spx;">%s</div>' % (path_count * 25, obj.name)
                else:
                    menudirc['html'] ='<div style="text-indent:%spx;">|__%s</div>' % (path_count * 25, obj.name)
            menulists.append(menudirc)
        return menulists


class ArticleCategory(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    path = models.CharField(max_length=255, null=True, blank=True)
    serialnumber=models.IntegerField(default=0)
    isvalid=models.BooleanField(default=True)
    path_id=models.CharField(max_length=255,null=True,blank=True)
    types=models.CharField(max_length=50,default='a')
    link = models.URLField(max_length=5000,default='')
    date=models.DateTimeField(auto_now_add=True)

    objects=models.Manager()
    menuobjects=ArticleCategoryManager()
    def __unicode__(self):
        if self.id == self.path:
            return self.name
        else:
            return self.node

    def _node(self):
        indent_num = len(self.path.split(':')) - 1
        indent = '....' * indent_num
        node = u'%s%s' % (indent, self.name)
        return node

    node = property(_node)

    class Meta:
        ordering = ['path']
    # 设置在model中的用途是，是在所有节点保存时递归的循环下去，更新所有的节点的路径
    def save(self, *args, **kwargs):
        # 先保存数据,如果是新添加的数据，放在第一行是用来获得id，因为id是path的重要组成
        super(ArticleCategory, self).save(*args, **kwargs)
        if self.parent:
            self.path = '%s:%s' % (self.parent.path, self.serialnumber)
            self.path_id = '%s:%s' % (self.parent.path_id, self.id)
            if not self.parent.isvalid:
                self.isvalid=self.parent.isvalid
        else:
            self.path ='%s' % (self.serialnumber)
            self.path_id = '%s' % (self.id)
        # 更新完当前节点path后，要进行一次保存，否则在编辑类别时，子分类循环保存父类path不是最新的
        super(ArticleCategory, self).save(*args, **kwargs)

        childrens = self.children.all()
        if len(childrens) > 0:
            for children in childrens:
                children.path = '%s:%s' % (self.path,children.serialnumber)
                children.path_id='%s:%s' % (self.path_id,children.id)
                if not self.isvalid:
                    children.isvalid = self.isvalid
                children.save()
class LeiXing(models.Model):
    name=models.CharField(max_length=50,null=False,blank=False)
    enable=models.BooleanField(default=False)




class Direction(models.Model):
    """
    方向：自动化，测试，运维，前端
    """
    name = models.CharField(verbose_name='名称', max_length=32)
    class Meta:
        db_table = 'Direction'
        verbose_name_plural = '方向（视频方向）'

    def __str__(self):
        return self.name


class Classification(models.Model):
    """
    分类：Python Linux JavaScript OpenStack Node.js
    """
    name = models.CharField(verbose_name='名称', max_length=32)

    class Meta:
        db_table = 'Classification'
        verbose_name_plural = '分类（视频分类）'

    def __str__(self):
        return self.name


class Level(models.Model):
    title = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '难度级别'

    def __str__(self):
        return self.title


class Video(models.Model):
    status_choice = (
        (0, '下线'),
        (1, '上线'),
    )

    status = models.IntegerField(verbose_name='状态', choices=status_choice, default=1)
    level = models.ForeignKey(Level)
    classification = models.ForeignKey('Classification', null=True, blank=True)

    weight = models.IntegerField(verbose_name='权重（按从大到小排列）', default=0)

    title = models.CharField(verbose_name='标题', max_length=32)
    summary = models.CharField(verbose_name='简介', max_length=32)
    # img = models.ImageField(verbose_name='图片', upload_to='static/images/Video')
    img = models.CharField(verbose_name='图片',max_length=32)
    href = models.CharField(verbose_name='视频地址', max_length=256)

    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Video'
        verbose_name_plural = '视频'

    def __str__(self):
        return self.title

