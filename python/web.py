import flask

app = flask.Flask(__name__)

@app.route( '/listView', methods=['GET'])
def listView():
    return flask.render_template('liveView.html')

@app.route('/vplayer', methods=['GET'])
def archive():
    return flask.render_template('vplayer.html')


app.run()