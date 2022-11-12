from src import cup_matches

from flask import Flask
from flask_restx import Resource, Api, fields
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = ["get"]

api = Api(app, version='1.0', title='World Cup Matches - NLW',
    description='World Cup Matches API')
ns = api.namespace('cupmatches', description='Calendar operations')

# Responses Model
date = api.model("Date", {
    "week": fields.String,
    "month": fields.String,
    "day": fields.Integer
})

teams = api.model("Teams", {
    "team1": fields.String,
    "team2": fields.String,
})

match = api.model("Match", {
    "teams": fields.Nested(teams),
    "time": fields.String,
})

matches = api.model("Matches", {
    "match": fields.List(fields.Nested(match)),
})

match_num = api.model("MatchesNumberByDate", {
    "date": fields.Nested(date),
    "match": fields.List(fields.Nested(match)),
})

all_matches = api.model("AllMatches", {
    "match_num": fields.Nested(match_num),
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
    @ns.doc(model=match_num)
    def get(self, match_num):
        return calendar.get_match(match_num)

@ns.route("/all_matches")
class AllMatch(Resource):
    @ns.doc(model=all_matches)
    def get(self):
        return calendar.get_all_matches()


if __name__ == "__main__":
    app.run()