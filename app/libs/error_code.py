"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from lin.exception import APIException


class BookNotFound(APIException):
    code = 404  # http状态码
    msg = '没有找到相关图书'  # 异常信息
    error_code = 80010  # 约定的异常码

    
class RefreshException(APIException):
    code = 401
    msg = "refresh token 获取失败"
    error_code = 10100


class ArticleNotFound(APIException):
    code=404
    msg='没有找到相关文章'
    error_code=80020

class ArticleCreateFailed(APIException):
    code=400
    msg='新建文章失败,数据库表字段未知异常'
    error_code=80021

class ArticleAlreadyExists(APIException):
    code=400
    msg='文章已存在,新建文章失败'
    error_code=80022

class ArticleUpdateFailed(APIException):
    code=400
    msg='文章更新失败'
    error_code=80023

class AppinfoNotFound(APIException):
    code=404
    msg='app版本信息未找到'
    error_code=80030

class AppinfoHasExists(APIException):
    code=400
    msg='app版本信息已存在'
    error_code=80031