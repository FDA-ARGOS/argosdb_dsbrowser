from flask_restx import Namespace, Resource, fields
from flask import (request, current_app)
from argosdb.document import get_one, get_many


api_name = "ngsfile"
api_desc = "NGS File APIs"

coll_name = "c_ngsfile"
main_id = "sra_run_id"
main_id_desc = "SRA Run ID"

search_title = "NGS File Search Query"
detail_title = "NGS File Detail Query"



api = Namespace(api_name, description=api_desc)

search_query_model = api.model(
    search_title, {'query': fields.String(required=True, default="", description='Query string')}
)

detail_query_model = api.model(
    detail_title, {main_id: fields.String(required=True, default="SRR123336", description=main_id_desc)}
)



@api.route('/search')
class Search(Resource):
    '''Search '''
    @api.doc('search')
    @api.expect(search_query_model)
    def post(self):
        '''Search '''
        req_obj = request.json
        req_obj["coll"] = coll_name
        res_obj = get_many(req_obj)
        return res_obj


@api.route('/detail')
class Detail(Resource):
    '''Detail '''
    @api.doc('detail')
    @api.expect(detail_query_model)
    def post(self):
        '''Detail '''
        req_obj = request.json
        req_obj["coll"] = coll_name
        res_obj = get_one(req_obj)
        return res_obj

