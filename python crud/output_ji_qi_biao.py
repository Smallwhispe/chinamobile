from sqlalchemy import String, Integer

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OutputJiQiBiao(db.Model):
    __tablename__ = 'output_ji_qi_biao'
    orderid = db.Column(String(45),primary_key=True)
    machineid = db.Column(String(45))
    workpieceid = db.Column(String(45))
    machineinformation = db.Column(String(45))

    def __repr__(self):
        return (f"OutputGongXuBiao(orderid='{self.orderid}', "
                f"machineid='{self.machineid}', "
                f"workpieceid='{self.workpieceid}', "
                f"machineinformation='{self.machineinformation}', ")
