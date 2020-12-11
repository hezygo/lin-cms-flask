# -*- encoding: utf-8 -*-
"""
@File :AppInfoManagment.py
@Description : app版本管理接口
@Date :2020/12/10 10:21:46
@Author :1573249948@qq.com
"""

from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success,Failed
from lin.redprint import Redprint
from lin.log import Logger
from app.models.AppVersionManage import AppVersion
from app.validators.forms import CreateAppInfo,SearchAppInfo,UpdateAppInfo


#app 版本信息管理
aim_api = Redprint('AppinfoManagment')


@aim_api.route('/',methods=['GET'])
@login_required
def get_all_info():
    """
    获取所有app版本信息
    ---
    tags:
    - app版本信息 API
    
    
    responses:
        200:
           description: 获取成功
           
        401:
           description: 认证失败

        404:
           description: 资源不存在

        500:
            description: 服务器异常
    """
    
    app_info= AppVersion.get_all_information()
    return jsonify(app_info)

@aim_api.route('/search',methods=['GET'])
@login_required
def get_info():
    """
    根据关键词查询app版本信息
    ---
    tags:
    - app版本信息 API

    parameters:
        - name: Model
          in: body
          type: string
          required: true
          description: 选择查询方式 例如`AppMarket`
        
        - name: KeyWord
          in: body
          type: string
          required: true
          description: 选择关键词 例如`应用宝`
    
    responses:
        200:
           description: 获取成功
           
        401:
           description: 认证失败

        404:
           description: 资源不存在
           
        500:
            description: 服务器异常
    """
    form=SearchAppInfo().validate_for_api()
    app_info= AppVersion.get_information(form)
    return jsonify(app_info)

@aim_api.route('/',methods=['POST'])
@login_required
def new_app_version_info():
    """
    新增app版本信息
    ---
    tags:
    - app版本信息 API
  
    parameters:
        - name: AppDescription
          in: body
          type: string
          required: true
          description: app 描述
        
        - name: AppMarket
          in: body
          type: string
          required: true
          description: app 商店名

        - name: AppName
          in: body
          type: string
          required: true
          description: app 包名称

        - name: AppPackageUrl
          in: body
          type: string
          required: true
          description: app url地址

        - name: AppVersion
          in: body
          type: string
          required: true
          description: app 版本号

    responses:
        200:
           description: 新建成功
           
        400:
           description: app 信息已存在
           
        500:
            description: 服务器异常
    """
    form =CreateAppInfo().validate_for_api()
    AppVersion.new_app_version(form)
    return Success('成功新建版本信息')

@aim_api.route('/<id>',methods=['DELETE'])
@Logger(template='{user.username}删除了一个app信息')
@login_required
def delete_app_version_info(id):
    """
    删除一个app版本信息
    ---
    tags:
    - app版本信息 API
    
    
    responses:
        200:
           description: app信息删除成功

        404:
           description: 资源不存在

        500:
            description: 服务器异常
    """
    AppVersion.delete_app_info(id)
    return Success('成功删除版本信息')

@aim_api.route('/<id>',methods=['PUT'])
@Logger(template='{user.username}更新了一个app信息')
@login_required
def update_app_version_info(id):
    """
    更新app版本信息
    ---
    tags:
    - app版本信息 API
  
    parameters:
        - name: AppDescription
          in: body
          type: string
          required: true
          description: app 描述
        
        - name: AppMarket
          in: body
          type: string
          required: true
          description: app 商店名

        - name: AppName
          in: body
          type: string
          required: true
          description: app 包名称

        - name: AppPackageUrl
          in: body
          type: string
          required: true
          description: app url地址

        - name: AppVersion
          in: body
          type: string
          required: true
          description: app 版本号
        
        - name: AppEnabled
          in: body
          type: boolean
          required: true
          description: app 是否上线

    responses:
        200:
           description: 更新成功
           
        400:
           description: app 信息无更新

        404:
           description: 资源不存在
           
        500:
            description: 服务器异常
    """
    form=UpdateAppInfo().validate_for_api()
    AppVersion.update_app_info(id,form)
    return Success('成功更新了`%s`的版本信息'%form.AppName.data)