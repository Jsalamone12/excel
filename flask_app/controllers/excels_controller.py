from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.excel_model import Excel
import pandas as pd


from flask import render_template, request, redirect, session, flash

@app.route('/dashboard')
def dashboard():

    if not 'uid' in session:
        flash('please log in')
        return redirect('/')
    
    logged_in_user = User.find_one_by_id(session['uid'])

    excels = Excel.get_with_users()

    return render_template("dashboard.html", user=logged_in_user, excels=excels)

@app.route('/new_excel')
def new_excel():
    if not 'uid' in session:
        flash('please log in first')
        return redirect('/')
    
    logged_in_user = User.find_one_by_id(session['uid'])

    return render_template('new_excel.html', user=logged_in_user)

@app.route('/create_excel', methods=['POST'])
def create_excel():
    # print (request.form)
    Excel.create(request.form)
    return redirect('/dashboard')


@app.route('/edit_excel/<int:id>')
def edit_excel(id):
    if not 'uid' in session:
        flash('please log in first')
        return redirect('/')
    
    logged_in_user = User.find_one_by_id(session['uid'])

    excel = Excel.find_one_by_id(id)

    return render_template('edit_excel.html', user=logged_in_user, excel=excel)


@app.route('/delete_excel/<int:id>')
def delete_excel(id):
    Excel.delete_by_id(id)

    return redirect('/dashboard')

@app.route('/save_excel', methods=['POST'])
def save_excel():
    # print(request.form)
    Excel.save(request.form)

    return redirect('/dashboard')

# @app.route('/join_tables', methods=['GET'])
# def join_tables():
#     engine = create_engine('mysql+pymysql://root:rootroot@localhost/mydatabase')
#     tableA = pd.read_sql_table('tableA', engine)
#     tableB = pd.read_sql_table('tableB', engine)
#     joined_table = pd.merge(tableA, tableB, on='name')
#     return joined_table.to_html()
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        # get the uploaded files
        file_a = request.files['file_a']
        file_b = request.files['file_b']
        
        # check if the files exist
        if not file_a or not file_b:
            flash('Please upload both files')
            return redirect(request.url)
        
        # read the files into pandas dataframes
        df_a = pd.read_excel(file_a)
        df_b = pd.read_excel(file_b)
        
        # perform the join operation
        result = pd.merge(df_a, df_b, on='name', how='inner')
        
        # create a new Excel file with the joined data
        Excel.create_from_dataframe(result)
        
        # redirect the user to the dashboard
        return redirect('/dashboard')
    
    # if the request method is GET, render the join.html template
    return render_template('join.html')

