from flask import Flask, jsonify, request
from flask_cors import CORS

# 导入Flask框架，用于创建Web应用；导入jsonify函数，用于生成JSON响应。
from output_ji_qi_biao import db,OutputJiQiBiao

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
@app.route('/machine/get', methods=['GET'])
# 定义一个路由处理函数，并将其与URL规则`/linklist`关联起来。这个路由将响应HTTP GET请求。
def get():
    # 定义一个函数，用于处理对`/linklist`路由的GET请求。
    links = OutputJiQiBiao.query.all()
    # 将查询结果转换为字典列表
    data = {'list':[{'orderid': link.orderid, 'machineid': link.machineid, 'workpieceid': link.workpieceid, 'machineinformation': link.machineinformation} for link in links]}
    # 返回JSON响应
    return jsonify(data)
    # 使用`jsonify`函数将字典列表转换为JSON格式的响应体，并返回给客户端。

@app.route('/machine/save', methods=['POST'])
def save():
    data = request.json
    new_item = OutputJiQiBiao(orderid=data['orderid'],machineid=data['machineid'],workpieceid=data['workpieceid'],machineinformation=data['machineinformation'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'orderid': new_item.orderid, 'number':new_item.number}), 200

@app.route('/machine/search', methods=['POST'])
def search():
    data = request.json
    query = OutputJiQiBiao.query  # 开始一个查询

    # 动态添加过滤条件
    if data.get('orderid') is not None and data['orderid'] != '':
        query = query.filter(OutputJiQiBiao.orderid == data['orderid'])
    if data.get('machineid') is not None and data['machineid'] != '':
        query = query.filter(OutputJiQiBiao.machineid == data['machineid'])
    if data.get('workpieceid') is not None and data['workpieceid'] != '':
        query = query.filter(OutputJiQiBiao.workpieceid == data['workpieceid'])
    if data.get('machineinformation') is not None and data['machineinformation'] != '':
        query = query.filter(OutputJiQiBiao.machineinformation == data['machineinformation'])

    links = query.all()  # 获取所有匹配的条目

    # 转换为字典格式以便返回
    results = {'list':[{'orderid': link.orderid, 'machineid': link.machineid, 'workpieceid': link.workpieceid, 'machineinformation': link.machineinformation} for link in links]}
    return jsonify(results), 200  # 返回所有匹配的条目

@app.route('/machine/delete', methods=['POST'])
def delete():
    data = request.json
    new_item = OutputJiQiBiao.query.get_or_404(data['orderid'])
    db.session.delete(new_item)
    db.session.commit()
    return jsonify({'orderid': new_item.orderid, 'machineid': new_item.machineid}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8182)
    # 如果这个脚本是作为主程序运行的（而不是被导入到其他脚本中），则启动Flask应用。
    # `debug=True`启用调试模式，`port=8182`指定应用监听的端口号。