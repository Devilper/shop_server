from peewee import *
from user_srv.settings import settings


class BasicModel(Model):
    class Meta:
        database = settings.DB


GENDER_CHOICE = (
    ("male", "男"),
    ("female", "女")
)

ROLE_CHOICE = (
    (1, "普通用户"),
    (2, "管理员")
)


class UserModel(BasicModel):
    user_id = AutoField(primary_key=True)
    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号")
    password = CharField(max_length=200, verbose_name="密码")
    nick_name = CharField(max_length=32, verbose_name="昵称", null=True)
    head_url = CharField(max_length=200, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=200, null=True, verbose_name="地址")
    desc = TextField(null=True, verbose_name="个人简介")
    gender = CharField(max_length=6, null=True, choices=GENDER_CHOICE, verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICE, verbose_name="用户角色")


if __name__ == '__main__':
    # 创建数据表
    # settings.DB.create_tables([UserModel])

    # from passlib.hash import pbkdf2_sha256
    # for i in range(10):
    #     user = UserModel()
    #     user.nick_name = f"fxm{i}"
    #     user.mobile = f"1314841376{i}"
    #     user.password = pbkdf2_sha256.hash("admin123")
    #     user.save()

    user = UserModel.select()
    print(user)
    for i in user:
        print(i.role)
