from sqlalchemy import String, Integer

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OutputGongXuBiao(db.Model):
    __tablename__ = 'output_gong_xu_biao'
    orderid = db.Column(String(45),primary_key=True)
    workpieceid = db.Column(String(45))
    processid = db.Column(String(45))
    machineid = db.Column(String(45))
    processtime = db.Column(Integer)  # 假设 processtime 为浮点数，代表时间

    def __repr__(self):
        return (f"OutputGongXuBiao(orderid='{self.orderid}', "
                f"workpieceid='{self.workpieceid}', "
                f"processid='{self.processid}', "
                f"machineid='{self.machineid}', "
                f"processtime={self.processtime})")
