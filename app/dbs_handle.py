from . import db

class Numerical_record(db.Model):
    __tablename__ = 'numerical_records'
    __table_args__ = {'extend_existing': True}
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    team_radiant = db.Column(db.Float(12), unique=False, nullable=False)
    radiant_1 = db.Column(db.Float(12), unique=False, nullable=False)
    radiant_2 = db.Column(db.Float(12), unique=False, nullable=False)
    radiant_3 = db.Column(db.Float(12), unique=False, nullable=False)
    radiant_4 = db.Column(db.Float(12), unique=False, nullable=False)
    radiant_5 = db.Column(db.Float(12), unique=False, nullable=False)
    team_dire = db.Column(db.Float(12), unique=False, nullable=False)
    dire_1 = db.Column(db.Float(12), unique=False, nullable=False)
    dire_2 = db.Column(db.Float(12), unique=False, nullable=False)
    dire_3 = db.Column(db.Float(12), unique=False, nullable=False)
    dire_4 = db.Column(db.Float(12), unique=False, nullable=False)
    dire_5 = db.Column(db.Float(12), unique=False, nullable=False)
    victory = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"Numerical_record('{self.match_id}', '{self.team_radiant}', '{self.radiant_1}',\
                                   '{self.radiant_2}', '{self.radiant_3}', '{self.radiant_4}',\
                                   '{self.radiant_5}', '{self.team_dire}', '{self.dire_1}',\
                                   '{self.dire_2}', '{self.dire_3}', '{self.dire_4}', '{self.dire5}', '{self.victory}')"


class League(db.Model):
    __tablename__ = 'leagues'
    __table_args__ = {'extend_existing': True}
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    league_id = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"League('{self.match_id}','{self.league_id}')"



class Score(db.Model):
    __tablename__ = 'scores'
    __table_args__ = {'extend_existing': True}
    player_hero = db.Column(db.String(45), primary_key=True, unique=True, nullable=False)
    success_score = db.Column(db.Float, nullable=False)
    exp = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Score('{self.player_hero}', '{self.success_score}', '{self.exp}')"


db.drop_all()
db.create_all()