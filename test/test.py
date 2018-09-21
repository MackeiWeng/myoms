# from flask import Flask, jsonify
# from flasgger import Swagger
# app = Flask(__name__)
# swagger = Swagger(app)
#
# @app.route('/colors/<palette>/')
# def colors(palette):
#     """Example endpoint returning a list of colors by palette This is using docstrings for specifications. --- parameters: - name: palette in: path type: string enum: ['all', 'rgb', 'cmyk'] required: true default: all definitions: Palette: type: object properties: palette_name: type: array items: $ref: '#/definitions/Color' Color: type: string responses: 200: description: A list of colors (may be filtered by palette) schema: $ref: '#/definitions/Palette' examples: rgb: ['red', 'green', 'blue']"""
#     all_colors = {
#      'cmyk': ['cian', 'magenta', 'yellow', 'black'],
#      'rgb': ['red', 'green', 'blue']
#      }
#     if palette =='all':
#         result = all_colors
#     else:
#         result = { palette: all_colors.get(palette) }
#     return jsonify(result)
# app.run(debug=True)


class test():
    __user = "test"
    _a = "a"

    def __init__(self):
        self.password = None


    # def password(self,passwd):
    #     print (self)
    #     print (passwd)

    def get_user(self,user=None):
        if user:
            print(id(self))
            print(user)
        else:
            print(id(self))
            print (self.__user)
            #print(__user)

    @property
    def passwd(self):
        raise AttributeError('`password` is not a readable attribute')

    @passwd.setter
    def passwd(self,password):
        print(self.__user)
        print(id(self))
        self.password = password
        print (self.password)

    @passwd.deleter
    def passwd(self):

        self.password = None



obj = test()
# print(id(obj))
# obj.passwd = "adminaa"
obj.get_user("dsfadf")
obj.get_user("aaaaa")
print ("输出class id",id(test))
test.get_user(test,"bbbb")
