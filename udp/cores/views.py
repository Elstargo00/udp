# udp/cores/views.py

from flask import render_template, request, Blueprint
from flask_login import login_required
from udp.functions import live_df_format, predict_ckpnt_model

cores = Blueprint('cores', __name__)

@cores.route('/')
def index():
    
    # # # # GET DATA UNTILS PREDICTION PIPELINE # # # #
    # preparing live match --> rows_live
    live_match = live_df_format()
    team_id_live = list()
    rows_live = list()
    for row in range(len(rows_live)):
        rows_live.append( ', '.join([str(item) for item in live_match.iloc[:,1:].values[row]]) )
        team_id_live.append( (live_match.iloc[:,1:].values[row][0], live_match.iloc[:,1:].values[row][6]) )
    # # # # # # # # # # # # # # # # # # #
    full_results = list()
    for i in range(len(rows_live)):
        result = predict_ckpnt_model(rows_live[i], team_id_live[i])
        full_results.append(result)
    # # # # # # # # # # # # # # # # # # #
    return render_template('index.html', full_results=full_results)


@cores.route('/home')
def home():
# check login:
# YES: check payment:
        # YES: go to "/home" (page for premium)
        # NO: go to "/go_premium" (page for register premium)
            # ask user for payment:
                # YES: pay and redirect them to /"home"
                # NO: redirect them to "/index"
# NO: redirect to login
    return render_template('home.html')


@cores.route('/go_premium')
def go_premium():
    pass











