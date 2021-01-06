from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from trends import main
import json
import plotly
import lp

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

@app.route("/blog/sample")
def blog_sample():
    return(render_template("blog/blog_sample.html"))

@app.route("/working_schedule", methods = ["GET"])
def working_schedule():
    group_one = int(request.args.get('groupOne'))
    group_two = int(request.args.get("groupTwo"))
    group_three = int(request.args.get("groupThree"))
    group_four = int(request.args.get("groupFour"))
    group_five = int(request.args.get("groupFive"))
    group_six = int(request.args.get("groupSix"))
    opt_x = lp.simple_working_schedule(group_one, group_two, group_three, group_four, group_five, group_six)
    return(render_template("lp_simple_solution.html", opt_x = list(map(round, opt_x))))

@app.route("/working_schedule_form")
def working_schedule_form():
    return(render_template("working_schedule_form.html"))

if __name__=="__main__":
    app.run(debug=False)