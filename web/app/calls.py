from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from models import Medic, Med, Customer, Checkup
import bleach

bp = Blueprint('calls', __name__, url_prefix='/calls')

PARAM_OF_CHECK = ['customer_id', 'symptom', 'place', 'diagnosis', 'comment', 'med_id', 'medic_id']

def params():
    dict_param_of_check = {}
    for p in PARAM_OF_CHECK:
        dict_param_of_check[p] = request.form.get(p)
    return dict_param_of_check

@bp.route('/new')
@login_required
def new():
    customers = Customer.query.all()
    meds = Med.query.all()
    medics = Medic.query.all()
    return render_template('calls/new.html', customers=customers, medics=medics, meds=meds)


@bp.route('/create', methods=['POST'])
@login_required
def create():

    checkup = Checkup(**params())

    if len(request.form.get('diagnosis')) == 0:
        flash('Заполните обязательное поле "Диагноз". Ошибка сохранения', 'danger')
        return redirect(url_for('calls.new'))

    try:
        db.session.add(checkup)
        db.session.commit()
    except:
        flash('Введите кореектные данные и проверьте заполнение всех полей. Ошибка сохранения', 'danger')
        return redirect(url_for('calls.new'))

    customers = request.form.getlist('customers')
    meds = request.form.getlist('meds')

    flash(f'Приём добавлен', 'success')

    return redirect(url_for('index'))

@login_required
@bp.route('/<int:checkup_id>')
def show(checkup_id):
    checkup = Checkup.query.get(checkup_id)

    return render_template('calls/templates/meds/show.html', checkup=checkup)
