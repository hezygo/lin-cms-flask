# -*- encoding: utf-8 -*-
"""
@File :article.py
@Description : 栏目文章接口
@Date :2020/12/07 16:52:43
@Author :1573249948@qq.com
"""


from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.Article import ArticleLibrary
from app.validators.forms import (
    BookSearchForm, CreateOrUpdateBookForm,
    CreateArticleForm, PublishArticle, ChangeActicleColumn
)

article_api = Redprint('article')


@article_api.route('/search', methods=['GET'])
@login_required
def search():
    form = BookSearchForm().validate_for_api()
    article = ArticleLibrary.search_by_keywords(form.q.data)
    return jsonify(article)


@article_api.route('/searchDeleted', methods=['GET'])
@login_required
def searchDeleted():
    # form = BookSearchForm().validate_for_api()
    article = ArticleLibrary.find_deleted_article()
    return jsonify(article)


@article_api.route('/', methods=['POST'])
@login_required
def create_article():
    form = CreateArticleForm().validate_for_api()
    ArticleLibrary.search_by_name(form)
    ArticleLibrary.new_article(form)
    return Success('新建文章成功')


@article_api.route('/', methods=['GET'])
@login_required
def get_all_article():
    """
    获取所有 文章资讯
    ---
    tags:
    - 资讯文章 API
    
    responses:
        200:
           description: 文章资讯更新成功

        404:
           description: 资源不存在

        500:
            description: 服务器异常
    """
    articles = ArticleLibrary.get_all()
    return jsonify(articles)


@article_api.route('/<id>', methods=['PUT'])
@login_required
def update_article(id):
    """
    更新 一篇文章资讯
    ---
    tags:
    - 资讯文章 API
    
    parameters:
        - name: IsOnline
          in: body
          type: Integer
          required: true
          description: 文章资讯的状态[0或1]
    
    responses:
        200:
           description: 文章资讯更新成功

        404:
           description: 资源不存在

        500:
            description: 服务器异常
    """
    form = CreateArticleForm().validate_for_api()
    ArticleLibrary.update_article(id, form)
    return Success(msg='更新文章成功')


@article_api.route('/<id>', methods=['DELETE'])
@login_required
def delete_article(id):
    """
    删除 一篇文章资讯
    ---
    tags:
    - 资讯文章 API
    
    responses:
        200:
           description: 文章资讯删除成功

        404:
           description: 资源不存在

        500:
            description: 服务器异常
    """
    ArticleLibrary.delete_article(id)
    return Success(msg='删除文章成功')


@article_api.route('/publish_or_take_offline_article/<id>', methods=['PUT'])
@login_required
def publish_or_take_offline_article(id):
    """
    上线或下线 一篇文章资讯
    ---
    tags:
    - 资讯文章 API
    
    parameters:
        - name: IsOnline
          in: body
          type: Integer
          required: true
          description: 文章资讯的状态[0或1]
    
    responses:
        200:
           description: 文章资讯上下线状态更改成功

        404:
           description: 资源不存在

        500:
            description: 服务器异常
    """
    form = PublishArticle().validate_for_api()
    is_online = int(form.IsOnline.data)
    ArticleLibrary.publish_article_now(id, is_online)
    if not is_online:
        return Success(msg='下线成功')
    return Success(msg='发布成功')


@article_api.route('/article_classification/<id>', methods=['PUT'])
def article_classification(id):
    """
    分类 一篇文章资讯
    ---
    tags:
    - 资讯文章 API

    parameters:
        - name: ActicleColumn
          in: body
          type: String
          required: true
          description: 文章资讯栏目名称
    
    responses:
        200:
           description: 文章资讯分类成功

        404:
           description: 资源不存在

        500:
            description: 服务器异常
    """
    form = ChangeActicleColumn().validate_for_api()
    ArticleLibrary.article_classification_query(id, form)
    return Success(msg='文章分类成功')
