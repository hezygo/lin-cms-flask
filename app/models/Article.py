# -*- encoding: utf-8 -*-
'''
@文件 :Article.py
@说明 :栏目文章管理
@时间 :2020/12/03 09:40:01
@作者 :1573249948@qq.com
'''

from app.libs.error_code import ArticleNotFound, ArticleCreateFailed, ArticleAlreadyExists, ArticleUpdateFailed
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, Unicode, BigInteger, DECIMAL, String, DateTime
from sqlalchemy.dialects.mssql import BIT, NTEXT
from datetime import datetime
import re

class ArticleLibrary(Base):
    """
    @description :文章栏目MODEL
    """
    __tablename__ = 'article_library'

    Id = Column('id', BigInteger, primary_key=True,
                autoincrement=True, nullable=False)
    Author = Column('author', Unicode(50), nullable=False)  # 作者
    Title = Column('title', Unicode(50), nullable=False)  # 标题
    ActicleSource = Column('acticle_source', Unicode(50), nullable=False)  # 来源
    ActicleColumn = Column('acticle_column', Unicode(50),
                           server_default='未分类文章')  # 栏目
    ArticleSummary = Column('article_summary', Unicode(), nullable=False)  # 摘要
    ActicleTarget = Column('acticle_target', Unicode(), nullable=False)  # 标签
    TumorTypes = Column('tumor_types', Unicode(50),
                        server_default='未分类')  # 肿瘤类型
    ActicleContent = Column(
        'acticle_content', Unicode(), nullable=False)  # 文章内容
    PublishDate = Column('publish_date', DateTime, nullable=False)  # 发布日期
    IsOnline = Column('is_online', Integer, default=int(0),
                      nullable=False)  # 是否上线

    @property
    def id(self):
        if self.Id is None:
            return None
        return self.Id

    @property
    def is_online(self):
        if self.IsOnline is None:
            return None
        return self.IsOnline

    @property
    def acticle_content(self):
        if self.ActicleContent is None:
            return None
        return self.ActicleContent

    @property
    def tumor_types(self):
        if self.TumorTypes is None:
            return None
        return self.TumorTypes

    @property
    def acticle_target(self):
        if self.ActicleTarget is None:
            return None
        return self.ActicleTarget

    @property
    def article_summary(self):
        if self.ArticleSummary is None:
            return None
        return self.ArticleSummary

    @property
    def acticle_column(self):
        if self.ActicleColumn is None:
            return None
        return self.ActicleColumn

    @property
    def publish_date(self):
        if self.PublishDate is None:
            return None
        return re.sub(r'\.\d+','',self.PublishDate)

    @property
    def author(self):
        if self.Author is None:
            return None
        return self.Author

    @property
    def title(self):
        if self.Title is None:
            return None
        return self.Title

    @property
    def acticle_source(self):
        if self.ActicleSource is None:
            return None
        return self.ActicleSource

    @classmethod
    def search_by_keywords(cls, q):
        articles = cls.query.filter(
            cls.Title.like('%' + q + '%')).all()
        if not articles:
            raise ArticleNotFound(msg='没有找到标题类似 `%s` 的文章' % q)
        return articles

    @classmethod
    def get_all(cls):
        """
        @description :查询所有文章
        @param :cls
        @return :文章详细信息
        """
        all_article = cls.query.filter_by(delete_time=None).all()
        if not all_article:
            raise ArticleNotFound(msg='没有相关文章')
        return all_article

    @classmethod
    def new_article(cls, form):
        """
        @description :插入新文章
        @param :form
        @return : True
        """
        publishDate = datetime.now(
        )  # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            cls.create(
                Author=form.Author.data,
                Title=form.Title.data,
                ActicleSource=form.ActicleSource.data,
                ArticleSummary=form.ArticleSummary.data,
                ActicleTarget=form.ActicleTarget.data,
                # TumorTypes=form.TumorTypes.data,
                ActicleContent=form.ActicleContent.data,
                PublishDate=publishDate,
                commit=True
            )
        except Exception as e:
            print('异常:'+e)
            raise ArticleCreateFailed()
        return True

    @classmethod
    def search_by_name(cls, form):
        title = form.Title.data
        name = cls.query.filter_by(Title=title).first()
        if name:
            raise ArticleAlreadyExists()

    @classmethod
    def update_article(cls, id_, form):
        article = cls.query.filter_by(Id=id_, delete_time=None).first()
        if not article:
            raise ArticleNotFound()
        try:
            article.update(
                Author=form.Author.data,
                Title=form.Title.data,
                # ActicleSource=form.ActicleSource.data,
                ArticleSummary=form.ArticleSummary.data,
                ActicleTarget=form.ActicleTarget.data,
                # TumorTypes=form.TumorTypes.data,
                ActicleContent=form.ActicleContent.data,
                commit=True
            )
        except Exception as e:
            print('异常:'+str(e))
            raise ArticleUpdateFailed()
        return True

    @classmethod
    def delete_article(cls, id_):
        """
        @description :软删除文章
        @param :id_ 文章id
        @return :
        """
        article = cls.query.filter_by(Id=id_, delete_time=None).first()
        if article is None:
            raise ArticleNotFound()
        article.delete(commit=True)
        return True

    @classmethod
    def find_deleted_article(cls):
        """
        @description :查找所有已删除的文章
        @param :
        @return :
        """
        article = cls.query.filter(cls.delete_time != None).all()
        if article is None:
            raise ArticleNotFound()
        return article

    @classmethod
    def publish_article_now(cls, id_, is_online):
        """
        @description :发布或下线文章
        @param : id_ 文章id
        @return :
        """

        article = cls.query.filter_by(Id=id_, delete_time=None).first()

        if article is None:
            raise ArticleNotFound()

        if article.IsOnline == is_online:
            msg = '文章已经下线'
            if is_online:
                msg = '文章已经上线'
            raise ArticleNotFound(msg=msg)

        if is_online:
            publishDate = datetime.now()
            article.update(
                IsOnline=is_online,
                PublishDate=publishDate,
                commit=True
            )
        else:
            article.update(
                IsOnline=is_online,
                commit=True
            )
        return

    @classmethod
    def article_classification_query(cls, id_, form):
        article = cls.query.filter_by(Id=id_, delete_time=None).first()
        if article is None:
            raise ArticleNotFound()
        # col_code=form.ActicleColumn.data
        # article_columns={
        #     '1':'假栏目'
        # }
        # if article.ActicleColumn==article_columns[col_code]:
        if article.ActicleColumn == form.ActicleColumn.data:
            raise ArticleNotFound(msg='文章的栏目已经为`'+article.ActicleColumn+'`')
        article.update(
            ActicleColumn=form.ActicleColumn.data,
            commit=True
        )
        return
