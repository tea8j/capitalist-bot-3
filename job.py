from quart import Quart, render_template

app = Quart(__name__)


@app.route('/')
async def root():
    return await render_template('index.html')


@app.route('/jobs/bird/<hexcode>')
async def bird(hexcode):
    return await render_template('bird.html', hexcode=hexcode)


app.run(host='0.0.0.0', port=80)
