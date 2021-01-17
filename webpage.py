from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
#from trends import plot
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
    from trends import plot
    plot = plot()
    ids = ['figure-{}'.format(i) for i, _ in enumerate(plot)]
    figuresJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('data.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route("/about")
def about():
    return(render_template("about.html"))

@app.route("/blog")
def blog():
    with open('blog_info.json') as f:
        blog_entries = json.load(f)
    return(render_template("blog/blog_index.html", blog_entries = blog_entries))

@app.route("/blog/lim_problem")
def blog_lim_problem():
    return(render_template("blog/lim_problem.html"))

@app.route("/blog/google_trends")
def unemployment_google():
    return(render_template("blog/google_trends.html"))

@app.route("/working_schedule_form")
def working_schedule_form():
    return(render_template("working_schedule_form.html"))

@app.route("/simple_working_schedule", methods = ["GET"])
def simple_working_schedule():
    group_one = int(request.args.get('groupOne'))
    group_two = int(request.args.get("groupTwo"))
    group_three = int(request.args.get("groupThree"))
    group_four = int(request.args.get("groupFour"))
    group_five = int(request.args.get("groupFive"))
    group_six = int(request.args.get("groupSix"))
    opt_x = lp.simple_working_schedule(group_one, group_two, group_three, group_four, group_five, group_six)   
    return(render_template("lp_simple_solution.html", opt_x = list(map(round, opt_x))))

@app.route("/milp_working_schedule", methods = ["POST"])
def milp_working_schedule():
    #if request.method == 'POST':
    #    fullname = request.form.getlist('field[]')
    #    for value in fullname:  
    #        print(value)    
    #min_wage = request.form['minHoursOne']
    min_hours = []
    max_hours = []
    hourly_wages = []
    availabilities = []
    num_employees = 8
    data = request.form
    fields = list(data)
    for field in range(0, (num_employees * 4), 4):
        min_hour = data[fields[field]] if data[fields[field]] != "" else 0
        min_hours.append(int(min_hour))
        max_hour = data[fields[field + 1]] if data[fields[field + 1]] != '' else 0
        max_hours.append(int(max_hour))
        hourly_wage =  data[fields[field + 2]] if data[fields[field + 2]] != '' else 0
        hourly_wages.append(int(hourly_wage))
        #availabilities.append(data[fields[field + 3]])
    print(min_hours)
    print(max_hours)
    print(hourly_wages)
    return(render_template("lp_milp_solution.html"))

if __name__=="__main__":
    app.run(debug = False)