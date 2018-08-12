from flask import render_template


def admin_dashboard():  # noqa: E501
    return render_template('admin/dashboard.html', title='Dashboard', page='Dashboard')

# def list_users():  # noqa: E501
#     return render_template('admin/dashboard.html', title='Dashboard')

