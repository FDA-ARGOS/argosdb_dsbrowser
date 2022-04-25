from flask_restx import Namespace, Resource, fields
from flask import (request, current_app)
from argosdb.document import get_one, get_many


api_name = "records"
api_desc = "Dataset Records APIs"

coll_name = "c_records"
main_id = "recordid"
main_id_desc = "Record ID"

search_title = "Dataset Records Search Query"
detail_title = "Dataset Records Detail Query"



api = Namespace(api_name, description=api_desc)

search_query_model = api.model(
    search_title, 
    {
        'bcoid': fields.String(required=False, default="ARGOS_000014", description='BCOID'),
        'filename': fields.String(required=False, default="sars-cov-2_lineage_mutations.tsv", description='Dataset file name'),
        'offset': fields.Integer(required=False, default=1, description='Page offset [1,2,3]'),
        'limit': fields.Integer(required=False, default=100, description='Page size')
    }
)

detail_query_model = api.model(
    detail_title, {main_id: fields.String(required=True, default="99287", description=main_id_desc)}
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

