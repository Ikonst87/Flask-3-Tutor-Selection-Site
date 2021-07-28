import random

from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

import database_funcs
import forms

app = Flask(__name__)
csrf = CSRFProtect(app)
secret_key = 'some_key_string'
app.config["SECRET_KEY"] = secret_key


@app.route("/")
def render_main():
    goals = database_funcs.get_data_from_json("goals")
    random_numbers = set()
    for i in range(10):
        if len(random_numbers) < 6:
            r = random.randint(0, 11)
            random_numbers.add(r)
        else:
            break
    teachers = database_funcs.get_data_from_json("teachers")
    teachers_flt = {}
    for n in random_numbers:
        teachers_flt[n] = teachers[str(n)]
    return render_template('index.html', goals=goals, teachers=teachers_flt)


@app.route("/all/", methods=["GET", "POST"])
def render_all_tutors():
    form = forms.SortForm()
    teachers = database_funcs.get_data_from_json("teachers")
    sort_order = request.form.get("comp_select")
    return render_template("all.html", form=form, sort_order=sort_order, teachers=teachers)


@app.route("/goals/<goal>/")
def render_goals(goal):
    try:
        goals = database_funcs.get_data_from_json("goals")[goal]
    except KeyError:
        error = f"Цели: {goal} не найдено в БД"
        return render_template("error.html", error=error), 404
    teachers = database_funcs.get_data_from_json("teachers")
    teachers_for_goal = {}
    for teacher_id, teacher_data in teachers.items():
        if goal in teacher_data["goals"]:
            teachers_for_goal[teacher_id] = teacher_data
    return render_template("goal.html", goal=goals, teachers=teachers_for_goal)


@app.route("/profile/<tutor_id>/")
def render_tutor_profile(tutor_id):
    tutors = database_funcs.get_data_from_json("teachers")
    try:
        tutor = tutors[tutor_id]
    except KeyError:
        error = f"Преподавателя с ID: {tutor_id} не найдено в БД"
        return render_template("error.html", error=error), 404
    goals = database_funcs.get_data_from_json("goals")
    weekdays = database_funcs.get_data_from_json("weekdays")
    busy_days = []
    for day, times in tutor["free"].items():
        if all(value == "False" for value in times.values()):
            busy_days.append(day)
    return render_template("profile.html", tutor=tutor, goals=goals, weekdays=weekdays, busy_days=busy_days,
                           tutor_id=tutor_id)


@app.route("/request/")
def render_request_form():
    form = forms.RequestForm()
    goals = database_funcs.get_data_from_json("goals")
    free_time = database_funcs.get_data_from_json("free_time")
    return render_template("request.html", form=form, goals=goals, free_time=free_time)


@app.route("/request_done/", methods=["POST"])
def render_success_request_form():
    form = forms.RequestForm()
    if form.validate():
        goal = request.form.get("goal")
        time = request.form.get("time")
        name = request.form.get("name")
        phone = request.form.get("phone")
        free_time = database_funcs.get_data_from_json("free_time")[time]
        goal = database_funcs.get_data_from_json("goals")[goal]
        selection_request = database_funcs.get_data_from_json("request")
        selection_request.append({"goal": goal["name"], "free_time": time, "name": name, "phone": phone})
        write_to_db = database_funcs.write_data_to_json("request", selection_request)
        if write_to_db == 'success':
            return render_template("request_done.html", goal=goal, free_time=free_time, name=name, phone=phone)
        else:
            error = f"Произошла ошибка при записи данных в БД"
            return render_template('error.html', error=error), 500
    else:
        phone_validation_error = form.phone.errors
        type_page = 'request_form'
        error = f"При заполнение формы произошла ошибка, телефон заполнен не верно:{phone_validation_error}"
        return render_template("error.html", error=error, type=type_page), 404


@app.route("/booking/<tutor_id>/<day_of_week>/<time>/", methods=["GET", "POST"])
def render_booking_form(tutor_id, day_of_week, time):
    form = forms.BookingForm()
    tutors = database_funcs.get_data_from_json("teachers")
    try:
        tutor = tutors[tutor_id]
    except KeyError:
        error = f"Преподавателя с ID: {tutor_id} не найдено в БД"
        return render_template("error.html", error=error), 404
    return render_template("booking.html", form=form, tutor=tutor, tutor_id=tutor_id, day=day_of_week, time=time)


@app.route("/booking_done/", methods=["GET", "POST"])
def render_success_booking_form():
    form = forms.BookingForm()
    if form.validate():
        time = form.time.data
        day = form.day.data
        name = form.name.data
        phone = form.phone.data
        tutor_id = form.tutor.data
        weekdays = database_funcs.get_data_from_json("weekdays")
        tutors = database_funcs.get_data_from_json("teachers")
        booking_requests = database_funcs.get_data_from_json("booking")
        booking_requests.append({"name": name, "phone": phone, "day": day, "time": time,
                                 "tutor": tutors[tutor_id]["name"]})
        try:
            tutors[tutor_id]["free"][day][time] = False
            write_to_db = database_funcs.write_data_to_json('teachers', tutors)
            write_to_db1 = database_funcs.write_data_to_json('booking', booking_requests)
            if write_to_db == 'success' and write_to_db1 == 'success':
                return render_template("booking_done.html", time=time, day=day, name=name, phone=phone,
                                       weekdays=weekdays, tutor=tutors[tutor_id]["name"])
            else:
                error = f"Произошла ошибка при записи данных в БД"
                return render_template('error.html', error=error), 500
        except KeyError:
            error = f"Указанный день: {day} и время {time} в расписание репититора не найдены"
            return render_template("error.html", error=error), 404
    else:
        phone_validation_error = form.name.errors
        type_page = 'booking_form'
        day = form.day.data
        tutor_id = form.tutor.data
        time = form.time.data
        error = f"При заполнение формы произошла ошибка, телефон заполнен не верно:{phone_validation_error}"
        return render_template("error.html", error=error, type=type_page, day=day, tutor_id=tutor_id, time=time)


if __name__ == '__main__':
    app.run(debug=True)
