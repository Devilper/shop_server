import grpc

from user_srv.proto import user_pb2_grpc, user_pb2


class UserTest:
    def __init__(self):
        # 连接grpc服务器
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(pn=2, pSize=5))
        print(rsp.total)
        for user in rsp.data:
            print(user.mobile, user.birthDay)

    def get_user_by_id(self):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserById(user_pb2.IdRequest(user_id=1))
        print(rsp)

    def get_user_by_mobile(self):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserByMobile(user_pb2.MobileRequest(mobile="13148413761"))
        print(rsp)

    def create_user(self):
        rsp: user_pb2.UserInfoResponse = self.stub.CreateUser(user_pb2.CreateUserInfo(
            nickName="haha",
            passWord="123456",
            Mobile="13148413710",
        ))
        print(rsp)

    def update_user(self):
        rsp: user_pb2.


if __name__ == '__main__':
    user = UserTest()
    # user.user_list()
    # user.get_user_by_id()
    # user.get_user_by_mobile()
    user.create_user()
