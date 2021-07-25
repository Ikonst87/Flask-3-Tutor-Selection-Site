from flask import Flask

app = Flask(__name__)


@app.route("/")
def render_main():
    return "Здесь будет главная страница"


@app.route("/all")
def render_all_tutors():
    return "Здесь будет страница со всеми преподавателями"


@app.route("/goals/<goal>/")
def render_goals(goal):
    return "Здесь будут <goal>"


@app.route("/profile/<tutor_id>/")
def render_tutor_profile(tutor_id):
    return "Здесь будет профиль репетитора"


@app.route("/request/")
def render_request_form():
    return "Здесь будет форма подбора репетиторов"


@app.route("/request_done")
def render_success_request_form():
    return "Здесь будет форма при успешном заполнение формы"


@app.route("/booking/<tutor_id>/<day_of_week>/<time>")
def render_booking_form():
    return "Здесь будет форма для бронирования занятий"


@app.route("/booking_done")
def render_success_booking_form():
    return "Здесь страница успешного бронирования занятия"


if __name__ == '__main__'
    app.run()