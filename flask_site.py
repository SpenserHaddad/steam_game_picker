from flask import Flask, render_template, request, url_for
import flask
import game_matcher

app = Flask(__name__)

@app.route('/')
def player_select():
    return render_template(r'player_search.html')

@app.route('/friends', methods=['GET', 'POST'])
def friends_list():
    # POST-Redirect-GET
    if request.method == 'POST':
        steam_name = request.form['steam_name']
        return flask.redirect(url_for('friends_list', player=steam_name))

    player = request.args['player']
    steam_id = game_matcher.get_steamid_from_name(player)
    friends = game_matcher.get_friends(steam_id)
    friend_ids = (f['steamid'] for f in friends)
    friend_names = (f['personaname'] for f in game_matcher.get_player_summaries(friend_ids))
    return render_template('friends.html', friend_names=friend_names)

if __name__ == "__main__":
    app.run(debug=True)

