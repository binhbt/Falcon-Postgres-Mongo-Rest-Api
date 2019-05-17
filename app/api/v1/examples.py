import falcon
import json
from app.model import ExampleModel
from app.errors import AppError, InvalidParameterError, UserNotExistsError, PasswordNotMatch


try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

class ExampleResource(object):
    def to_json(self, body_dict):
        return json.dumps(body_dict)

    def on_success(self, res, data=None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta['code'] = 200
        meta['message'] = 'OK'

        obj = OrderedDict()
        obj['meta'] = meta
        obj['data'] = data
        res.body = self.to_json(obj)

    def on_get(self, req, resp):
        rows = []
        for i in ExampleModel.objects:
            row = {
                'email': i.email,
                'name': i.name
            }
            rows.append(row)

        if rows:
            obj = [user for user in rows]
            self.on_success(resp, obj)
        else:
            raise AppError()


    def on_post(self, req, resp):
        user_req = req.context['data']
        email = user_req['email']
        name = user_req['name']

        row = ExampleModel(
            email = email,
            name = name
        )
        row.save()

        resp.json = {'id': str(row.id)}
        resp.status = falcon.HTTP_201
