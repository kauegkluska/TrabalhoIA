from flask import Blueprint, render_template

bp = Blueprint("pages", __name__)

#renderiza a página inicial
@bp.route("/")
def index():
    return render_template("index.html")
