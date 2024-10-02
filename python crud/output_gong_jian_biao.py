from sqlalchemy import String, Integer

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OutputGongJianBiao(db.Model):
    __tablename__ = 'output_gong_jian_biao'
    orderid = db.Column(String(45),primary_key=True)
    workpieceid = db.Column(String(45))
    number = db.Column(Integer)
    workpieceinformation = db.Column(String(45))

    def __repr__(self):
        return (f"OutputGongJianBiao(orderid='{self.orderid}', "
                f"workpieceid='{self.workpieceid}', "
                f"number='{self.number}', "
                f"workpieceinformation={self.workpieceinformation})")
