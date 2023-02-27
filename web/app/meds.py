from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from models import Med
import bleach

bp = Blueprint('meds', __name__, url_prefix='/meds')

PARAM_OF_CHECK = ['name', 'description', 'way', 'side']

PARAM_OF_REVIEW = ['id', 'name', 'description', 'way', 'side']

def params():
    dict_param_of_check = {}
    for p in PARAM_OF_CHECK:
        dict_param_of_check[p] = request.form.get(p)
    return dict_param_of_check

def params_review():
    dict_param_of_review = {}
    for p in PARAM_OF_REVIEW:
        dict_param_of_review[p] = request.form.get(p)
    return dict_param_of_review

@bp.route('/new')
@login_required
def new():
    return render_template('meds/new.html')


@bp.route('/create', methods=['POST'])
@login_required
def create():

    med = Med(**params())

    if len(request.form.get('name')) == 0:
        flash('Заполните обязательное поле "Название". Ошибка сохранения', 'danger')
        return redirect(url_for('meds.new'))
    if len(request.form.get('description')) == 0:
        flash('Заполните обязательное поле "Описание". Ошибка сохранения', 'danger')
        return redirect(url_for('meds.new'))
    if len(request.form.get('way')) == 0:
        flash('Заполните обязательное поле "Способ применения". Ошибка сохранения', 'danger')
        return redirect(url_for('meds.new'))
    if len(request.form.get('side')) == 0:
        flash('Заполните обязательное поле "Побочные эффекты". Ошибка сохранения', 'danger')
        return redirect(url_for('meds.new'))

    try:
        db.session.add(med)
        db.session.commit()
    except:
        flash('Введите кореектные данные и проверьте заполнение всех полей. Ошибка сохранения', 'danger')
        return redirect(url_for('meds.new'))

    flash(f'Лекарство добавлено', 'success')

    return redirect(url_for('index'))

# @bp.route('/find')
# @login_required
# def find():
#     return render_template('meds/find.html')


@bp.route('/search', methods=['GET'])
@login_required
def search():

    med = Med(**params_review())
    try:
        db.session.query.query(Med.id, Med.name).all()
    except:
        flash('Введите кореектные данные и проверьте заполнение всех полей. Ничего не найдено', 'danger')
        return redirect(url_for('calls.new'))

    flash(f'Лекарство найдено', 'success')

    return redirect(url_for('show', id=med.id))

@login_required
@bp.route('/<int:id>')
def show(id):
    med = Med.query.get(id)

    return render_template('/meds/show.html', med=med)