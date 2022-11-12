from src import cup_matches

from flask import Flask
from flask_restx import Resource, Api, fields
# from flask_cors import CORS


app = Flask(__name__)
app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = ["get"]

# CORS(app)
api = Api(app, version='1.0', title='World Cup Matches - NLW',
    description='World Cup Matches API')
ns = api.namespace('cupmatches', description='Calendar operations')


my_model = api.model('MyModel', {
    'match_num': fields.Integer(description='The match number', required=True, min=0),
})


class CupCalendarAPI(object):
    def get_match(self, match_num):
        match = cup_matches.get_matches_by_num(match_num)
        if match:
            return (match, 200)
        api.abort(404, "Match {} doesn't exist".format(match_num))
    
    def get_all_matches(self):
        all_match = cup_matches.get_all_matches()
        if all_match:
            return (all_match, 200)
        api.abort(404, "Error the searching all matches")


calendar = CupCalendarAPI()


@ns.route('/<int:match_num>')
@api.doc(params={'match_num': 'The match number'})
class MatchByNumber(Resource):
    @ns.doc(model=my_model)
    @api.response(200, '\{\"date\": \{\}, \"matches\": \{\"match_num\": \{\"teams\": \{\}\}\}\}')
    def get(self, match_num):
        return calendar.get_match(match_num)

@ns.route("/all_matches")
class AllMatch(Resource):
    def get(self):
        return calendar.get_all_matches()


if __name__ == "__main__":
    app.run()