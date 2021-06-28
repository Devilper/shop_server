import time
from datetime import date

import grpc
from loguru import logger
from peewee import DoesNotExist
from passlib.hash import pbkdf2_sha256
from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.model.models import UserModel
from google.protobuf.empty_pb2 import Empty


class UserServicer(user_pb2_grpc.UserServicer):
    def convert_user_to_rsp(self, user):
        # 处理user用户信息
        user_info_rsp = user_pb2.UserInfoResponse()

        user_info_rsp.user_id = user.user_id
        user_info_rsp.mobile = user.mobile
        user_info_rsp.role = user.role
        user_info_rsp.passWord = user.password

        if user.nick_name:
            user_info_rsp.nickName = user.nick_name
        if user.gender:
            user_info_rsp.gender = user.gender
        if user.birthday:
            user_info_rsp.birthDay = int(time.mktime(user.birthday.timetuple()))
        return user_info_rsp

    @logger.catch
    def GetUserList(self, request: user_pb2.PageInfo, context):
        # 获取用户列表

        rsp = user_pb2.UserListResponse()  # 获取返回数据结构

        users = UserModel.select()
        rsp.total = users.count()

        # 分页
        page = 1
        per_page_nums = 10
        if request.pSize:
            per_page_nums = request.pSize
        if request.pn:
            page = request.pn
        start = per_page_nums * (page - 1)
        users = users.limit(per_page_nums).offset(start)
        # 遍历数据集
        for user in users:
            rsp.data.append(self.convert_user_to_rsp(user))
        return rsp

    @logger.catch
    def GetUserById(self, request: user_pb2.IdRequest, context):
        # 通过user_id获取用户信息
        try:
            user = UserModel.get(UserModel.user_id == request.user_id)
            return self.convert_user_to_rsp(user)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def GetUserByMobile(self, request: user_pb2.MobileRequest, context):
        # 通过mobile获取用户信息
        try:
            user = UserModel.get(UserModel.mobile == request.mobile)
            return self.convert_user_to_rsp(user)

        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def CreateUser(self, request: user_pb2.CreateUserInfo, context):
        try:
            UserModel.get(UserModel.mobile == request.Mobile)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("用户已存在")
            return user_pb2.UserInfoResponse()

        except DoesNotExist as e:
            ...

        user = UserModel()
        logger.debug(request.nickName)
        user.nick_name = request.nickName
        logger.debug(request.Mobile)
        user.mobile = request.Mobile
        logger.debug(request.passWord)
        user.password = pbkdf2_sha256.hash(request.passWord)
        user.save()

        return self.convert_user_to_rsp(user)

    @logger.catch
    def UpdateUsr(self, request: user_pb2.UpdateUserInfo, context):
        # 修改用户信息
        try:
            user = UserModel.get(UserModel.user_id == request.user_id)
            user.nick_name = request.nickName
            user.gender = request.gender
            user.birthday = date.fromtimestamp(request.birthDay)
            user.save()
            return Empty()

        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()
