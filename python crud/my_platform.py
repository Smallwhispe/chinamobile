from sqlalchemy import String

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 假设我们有一个简单的用户表
class Platform(db.Model):
    __tablename__ = 'production_order'
    appid = db.Column(String(45), primary_key=True)
    zuoyelingdanhao = db.Column(String(45))
    linshilingdanhao = db.Column(String(45))


    # __repr__方法定义了如何打印User实例的字符串表示形式，这在进行调试时非常有用。
    def __repr__(self):
        return f"ProductionOrder(appid='{self.appid}', zuoyelingdanhao='{self.zuoyelingdanhao}', linshilingdanhao='{self.linshilingdanhao}')"