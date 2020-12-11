# -*- encoding: utf-8 -*-
"""
@File :AppVersionManage.py
@Description : App版本管理
@Date :2020/12/10 10:03:39
@Author :1573249948@qq.com
"""

from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Unicode, BigInteger, and_
from sqlalchemy.dialects.mssql import BIT, DATETIME2
from app.libs.error_code import AppinfoNotFound, AppinfoHasExists
from flask_jwt_extended import get_current_user
from datetime import datetime


class AppVersion(Base):
    """ 
    @description Lighthouse App 版本管理 
    """

    #
    __tablename__ = 'app_info'

    _Id = Column('Id', BigInteger, primary_key=True,
                 autoincrement=True, nullable=False)
    AppName = Column('Name', Unicode(10))
    AppVersion = Column('Version', Unicode(30))
    AppOS = Column('OS', Unicode(30), nullable=False)
    _AppMarket = Column('AppMarket', Unicode(50))
    AppPublishTime = Column('PublishTime', DATETIME2(7))
    AppDescription = Column('Description', Unicode())
    AppEnabled = Column('Enabled', BIT(), nullable=False,
                        server_default='true')
    AppPackageUrl = Column('PackageUrl', Unicode(1000))
    AppEditor = Column('Editor', Unicode(20))

    @property
    def PackageUrl(self):
        if self.AppPackageUrl is None:
            return None
        return self.AppPackageUrl

    @property
    def Description(self):
        if self.AppDescription is None:
            return None
        return self.AppDescription

    @property
    def Name(self):
        if self.AppName is None:
            return None
        return self.AppName

    @property
    def Editor(self):
        if self.AppEditor is None:
            return None
        return self.AppEditor

    @property
    def PublishTime(self):
        if self.AppPublishTime is None:
            return None
        return self.AppPublishTime

    @property
    def AppMarket(self):
        if self._AppMarket is None:
            return None
        return self._AppMarket

    @property
    def Id(self):
        if self._Id is None:
            return None
        return self._Id

    @property
    def OS(self):
        if self.AppOS is None:
            return None
        return self.AppOS

    @property
    def Version(self):
        if self.AppVersion is None:
            return None
        return self.AppVersion

    @property
    def Enabled(self):
        if self.AppEnabled is None:
            return None
        return self.AppEnabled

    @classmethod
    def get_all_information(cls):
        app_info = cls.query.filter_by(delete_time=None).all()
        if not app_info:
            raise AppinfoNotFound()
        return app_info

    @classmethod
    def new_app_version(cls, form):
        # 在使用and_和or_的时候要用filter
        app_v = cls.query.filter(
            and_(
                cls.AppOS == form.AppOS.data,
                cls._AppMarket == form.AppMarket.data,
                cls.AppVersion == form.AppVersion.data
            )
        ).first()
        if app_v:
            raise AppinfoHasExists()
        user = get_current_user()
        editor = user.username
        app_publish_time = datetime.now()
        cls.create(
            AppName=form.AppName.data,
            AppOS=form.AppOS.data,
            _AppMarket=form.AppMarket.data,
            AppPublishTime=app_publish_time,
            AppDescription=form.AppDescription.data,
            # AppEnabled=form.AppEnabled.data,
            AppPackageUrl=form.AppPackageUrl.data,
            AppVersion=form.AppVersion.data,
            AppEditor=editor,
            commit=True
        )
        return

    @classmethod
    def update_app_info(cls, info_id, form):
        app_info = cls.query.filter_by(_Id=info_id, delete_time=None).first()
        if app_info is None:
            raise AppinfoNotFound()
        if cls.compare_value(cls,form):
            raise AppinfoHasExists('没有任何更新')
        user = get_current_user()
        editor = user.username
        app_info.update(
            AppName=form.AppName.data if app_info.AppName != form.AppName.data else app_info.AppName,
            AppVersion=form.AppVersion.data if app_info.AppVersion != form.AppVersion.data else app_info.AppVersion,
            AppOS=form.AppOS.data if app_info.AppOS != form.AppOS.data else app_info.AppOS,
            _AppMarket=form.AppMarket.data if app_info._AppMarket != form.AppMarket.data else app_info._AppMarket,
            AppEnabled=form.AppEnabled.data if app_info.AppEnabled != form.AppEnabled.data else app_info.AppEnabled,
            AppDescription=form.AppDescription.data if app_info.AppDescription != form.AppDescription.data else app_info.AppDescription,
            AppPackageUrl=form.AppPackageUrl.data if app_info.AppPackageUrl != form.AppPackageUrl.data else app_info.AppPackageUrl,
            AppEditor=editor,
            commit=True
        )
        return

    @classmethod
    def delete_app_info(cls, info_id):
        app_info = cls.query.filter_by(_Id=info_id, delete_time=None).first()
        if app_info is None:
            raise AppinfoNotFound()
        app_info.update(
            delete_time=datetime.now(),
            commit=True
        )
        return

    @classmethod
    def get_information(cls, form):
        model = form.Model.data
        if model=='AppMarket':
            model='_%s'%model
        q = 'cls.%s==form.KeyWord.data' % model
        app_info = cls.query.filter(eval(q),cls.delete_time==None).all()
        if not app_info:
            raise AppinfoNotFound()
        return app_info

    def compare_value(self,form):
        app_info=self.query.filter(and_(
            self.AppName == form.AppName.data,
            self.AppVersion == form.AppVersion.data,
            self.AppOS == form.AppOS.data,
            self._AppMarket == form.AppMarket.data,
            self.AppEnabled == form.AppEnabled.data,
            self.AppDescription == form.AppDescription.data,
            self.AppPackageUrl == form.AppPackageUrl.data
        )).first()
        return app_info
        
        
