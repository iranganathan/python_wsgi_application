# -*- coding: utf-8 -*-
from engine import render, print_error
import queries


def index(context):
    return render('index.html', {'title': 'Home page'})


def add_region(context):
    cur = context.cursor
    alert = ' '

    try:
        name = context.POST.get('name', [''])[0]
        if name != '':
            cur.execute(queries.add_region, {"region_name": name}, commit=True)
            alert = '<p><span style="color: red;">Region %s has been added!</span></p>' % name
    except:
        print_error()

    return render('add_region.html', {'title': 'Add region', 'alert': alert})


def add_city(context):
    cur = context.cursor
    regions = cur.execute(queries.get_all_regions)

    alert = ' '
    regions_html = ''
    for row in regions:
        regions_html += '<option value=%s>%s</option>' % (row['id_region'], row['name'])

    try:
        id_region = context.POST.get('region', [''])[0]
        name = context.POST.get('name', [''])[0]
        if name != '':
            cur.execute(queries.add_city, {"id_region": id_region, "city_name": name}, commit=True)
            alert = '<p><span style="color: red;">City %s has been added!</span></p>' % name
    except:
        print_error()

    return render('add_city.html', {'title': 'Add city', 'regions': regions_html, 'alert': alert})


def send_feedback(context):
    cur = context.cursor
    regions = cur.execute(queries.get_all_regions)

    alert = ' '
    regions_html = ''
    for row in regions:
        regions_html += '<option value=%s>%s</option>' % (row['id_region'], row['name'])

    try:
        last_name = context.POST.get('last_name', [''])[0]
        first_name = context.POST.get('first_name', [''])[0]
        id_region = context.POST.get('region', [''])[0]
        id_city = context.POST.get('city', [''])[0]
        phone = context.POST.get('phone', [''])[0].replace(' ', '+')
        email = context.POST.get('email', [''])[0]
        message = context.POST.get('message', [''])[0]

        if last_name != '' and first_name != '' and message != '':
            cur.execute(queries.add_feedback, {"last_name": last_name, "first_name": first_name,
                                               "id_region": int(id_region), "id_city": int(id_city),
                                               "phone": phone, "email": email, "message": message}, commit=True)
            alert = '<p><span style="color: red;">Your feedback has been sent!</span></p>'
    except:
        print_error()

    return render('send_feedback.html', {'title': 'Send feedback', 'regions': regions_html, 'alert': alert})


def region(context):
    cur = context.cursor
    action = context.GET.get('action', [''])[0]
    id = context.GET.get('id', [0])[0]
    if action == 'delete' and id != 0:
        cur.execute(queries.delete_region, {"id_region": id}, commit=True)

    regions = cur.execute(queries.get_all_regions)

    regions_html = ''
    for row in regions:
        row['action'] = '<a href="/region?action=delete&id=%s">Delete</a>' % row['id_region']
        regions_html += """
            <tr>
            <td>%(id_region)s</td>
            <td>%(name)s</td>
            <td>%(action)s</td>
            </tr>
        """ % row

    return render('region.html', {'title': 'Regions', 'regions_table': regions_html})


def city(context):
    cur = context.cursor
    action = context.GET.get('action', [''])[0]
    id = context.GET.get('id', [0])[0]
    if action == 'delete' and id != 0:
        cur.execute(queries.delete_city, {"id_city": id}, commit=True)

    cities = cur.execute(queries.get_all_cities)

    cities_html = ''
    for row in cities:
        row['action'] = '<a href="/city?action=delete&id=%s">Delete</a>' % row['id_city']
        cities_html += """
            <tr>
            <td>%(id_city)s</td>
            <td>%(region_name)s</td>
            <td>%(city_name)s</td>
            <td>%(action)s</td>
            </tr>
        """ % row

    return render('city.html', {'title': 'Cities', 'cities_table': cities_html})


def feedback(context):
    cur = context.cursor
    action = context.GET.get('action', [''])[0]
    id = context.GET.get('id', [0])[0]
    if action == 'delete' and id != 0:
        cur.execute(queries.delete_feedback, {"id_feedback": id}, commit=True)

    feedback_list = cur.execute(queries.get_all_feedback)

    feedback_html = ''
    for row in feedback_list:
        row['action'] = '<a href="/feedback?action=delete&id=%s">Delete</a>' % row['id_feedback']
        row['city_name'] = row['city_name'] or ''
        row['region_name'] = row['region_name'] or ''
        feedback_html += """
            <tr>
            <td>%(id_feedback)s</td>
            <td>%(last_name)s</td>
            <td>%(first_name)s</td>
            <td>%(region_name)s</td>
            <td>%(city_name)s</td>
            <td>%(phone)s</td>
            <td>%(email)s</td>
            <td>%(message)s</td>
            <td>%(action)s</td>
            </tr>
        """ % row

    return render('feedback.html', {'title': 'Feedback', 'feedback_table': feedback_html})


def statistics(context):
    cur = context.cursor

    regions = cur.execute(queries.get_regions_with_feedback_count)

    regions_html = ''
    counter = 1
    for row in regions:
        if row['region_name'] is not None:
            row['counter'] = counter
            regions_html += """
                <tr>
                <td>%(counter)s</td>
                <td>%(region_name)s</td>
                <td>%(cnt)s</td>
                </tr>
            """ % row
            counter += 1

    regions_filtered = cur.execute(queries.get_regions_with_feedback_count_greater, {"feedback_count": 2})

    regions_filtered_html = ''
    counter = 1
    for row in regions_filtered:
        if row['region_name'] is not None:
            row['counter'] = counter
            regions_filtered_html += """
                <tr>
                <td>%(counter)s</td>
                <td>%(region_name)s</td>
                <td>%(cnt)s</td>
                </tr>
            """ % row
            counter += 1

    cities = cur.execute(queries.get_cities_and_feedback_count)

    cities_html = ''
    no_city = 0
    for row in cities:
        if row['city_name'] is None:
            no_city = row['count']
        else:
            cities_html += """
                <tr>
                <td>%(id_city)s</td>
                <td>%(region_name)s</td>
                <td>%(city_name)s</td>
                <td>%(cnt)s</td>
                </tr>
            """ % row

    return render('statistics.html', {'title': 'Statistics', 'regions': regions_html,
                                      'regions_filtered': regions_filtered_html, 'cities': cities_html,
                                      'no_city': no_city})


def get_data(context):
    cur = context.cursor
    category = context.POST.get('category', [''])[0]
    response_html = ''

    if category == 'cities':
        id_region = context.POST.get('id', [0])[0]
        cities = cur.execute(queries.get_all_cities_in_region, {"id_region": id_region})
        for row in cities:
            response_html += '<option value=%(id_city)s>%(name)s</option>' % row

    return response_html


def error_404(context):
    return render(parameters={'title': '404: Not Found'})


def error_500(context):
    return render(parameters={'title': '500: Internal Server Error'})
