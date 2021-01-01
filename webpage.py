from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from trends import main
import json
import plotly

app = Flask(__name__)

@app.route("/")
def home():
    return(render_template("index.html"))

#think of changing name
@app.route("/data")
def plot():
    plot = main()
    ids = ['figure-{}'.format(i) for i, _ in enumerate(plot)]
    figuresJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('data.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
                        
@app.route("/blog")
def blog():
    with open('blog_info.json') as f:
        blog_entries = json.load(f)
    return(render_template("blog/blog_index.html", blog_entries = blog_entries))

@app.route("/blog/lim_problem")
def blog_lim_problem():
    return(render_template("blog/lim_problem.html"))


if __name__=="__main__":
    app.run(debug=False)