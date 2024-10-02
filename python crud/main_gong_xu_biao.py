from flask import Flask, jsonify, request
from flask_cors import CORS

# 导入Flask框架，用于创建Web应用；导入jsonify函数，用于生成JSON响应。
from output_gong_xu_biao import db,OutputGongXuBiao

app = Flask(__name__)
# 创建一个Flask应用实例。`__name__`是当前模块的名称，Flask使用它来找到应用的位置，从而知道在哪里可以找到资源文件（如模板和静态文件）。

# 配置数据库URI（这里使用SQLite作为示例）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sfzhm130928@localhost:3306/platform'
# 设置SQLAlchemy的配置选项，指定数据库URI。

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 禁用SQLAlchemy的事件系统，减少不必要的内存开销。这是一个推荐的做法，特别是在生产环境中。
db.init_app(app)
with app.app_context():
    db.create_all()

cors = CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True,
                                                    "methods": ["GET", "POST"],
                                    "allow_headers": ["Content-Type", "Authorization"]}})
# 使用Flask应用上下文来确保能够正确地与数据库交互。`db.create_all()`方法会检查数据库中是否存在所有定义的模型表，如果不存在，则根据模型定义创建它们。

# 路由处理函数
@app.route('/process/get', methods=['GET'])
# 定义一个路由处理函数，并将其与URL规则`/linklist`关联起来。这个路由将响应HTTP GET请求。
def get():
    # 定义一个函数，用于处理对`/linklist`路由的GET请求。
    links = OutputGongXuBiao.query.all()
    # 将查询结果转换为字典列表
    data = {'list':[{'orderid': link.orderid, 'workpieceid': link.workpieceid, 'processid': link.processid, 'machineid': link.machineid, 'processtime': link.processtime} for link in links]}
    # 返回JSON响应
    return jsonify(data)
    # 使用`jsonify`函数将字典列表转换为JSON格式的响应体，并返回给客户端。

@app.route('/process/save', methods=['POST'])
def save():
    data = request.json
    new_item = OutputGongXuBiao(orderid=data['orderid'],workpieceid=data['workpieceid'],processid=data['processid'],machineid=data['machineid'],processtime=data['processtime'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'orderid': new_item.orderid, 'processtime':new_item.processtime}), 200

@app.route('/process/search', methods=['POST'])
def search():
    data = request.json
    query = OutputGongXuBiao.query  # 开始一个查询

    # 动态添加过滤条件
    if data.get('orderid') is not None and data['orderid'] != '':
        query = query.filter(OutputGongXuBiao.orderid == data['orderid'])
    if data.get('workpieceid') is not None and data['workpieceid'] != '':
        query = query.filter(OutputGongXuBiao.workpieceid == data['workpieceid'])
    if data.get('processid') is not None and data['processid'] != '':
        query = query.filter(OutputGongXuBiao.processid == data['processid'])
    if data.get('machineid') is not None and data['machineid'] != '':
        query = query.filter(OutputGongXuBiao.machineid == data['machineid'])
    if data.get('processtime') is not None and data['processtime'] != '':
        query = query.filter(OutputGongXuBiao.processtime == data['processtime'])

    items = query.all()  # 获取所有匹配的条目

    # 转换为字典格式以便返回
    results = {'list':[{'orderid': link.orderid, 'workpieceid': link.workpieceid, 'processid': link.processid, 'machineid': link.machineid, 'processtime': link.processtime} for link in items]}
    return jsonify(results), 200  # 返回所有匹配的条目

@app.route('/process/delete', methods=['POST'])
def delete():
    data = request.json
    new_item = OutputGongXuBiao.query.get_or_404(data['orderid'])
    db.session.delete(new_item)
    db.session.commit()
    return jsonify({'orderid': new_item.orderid, 'workpieceid': new_item.workpieceid}), 200


# def delete_item():
#     data = request.json
#     print(data)
#
#     # 尝试从请求中获取任意字段
#     query = OutputGongXuBiao.query
#
#     if 'orderid' in data:
#         query = query.filter_by(orderid=data['orderid'])
#     if 'processid' in data:
#         query = query.filter_by(processid=data['processid'])
#     if 'processtime' in data:
#         query = query.filter_by(processtime=data['processtime'])
#     if 'machineid' in data:
#         query = query.filter_by(machineid=data['machineid'])
#     if 'workpieceid' in data:
#         query = query.filter_by(workpieceid=data['workpieceid'])
#
#     # 获取条目，若不存在则返回404
#     item_to_delete = query.first_or_404()
#     print(item_to_delete)
#
#     db.session.delete(item_to_delete)
#     db.session.commit()
#
#     return jsonify({'orderid': item_to_delete.orderid, 'workpieceid': item_to_delete.workpieceid}), 200
if __name__ == '__main__':
    app.run(debug=True, port=8181)
    # 如果这个脚本是作为主程序运行的（而不是被导入到其他脚本中），则启动Flask应用。
    # `debug=True`启用调试模式，`port=8181`指定应用监听的端口号。