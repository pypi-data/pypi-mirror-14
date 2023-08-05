import xml.etree.ElementTree as ET
import json
import xlwt
import datetime

from django.shortcuts import render
from django.db import connection
from django.db import connections
from decimal import Decimal
from django.http import HttpResponse
from django.conf import settings
from operator import indexOf
from datetime import date

try:
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import green, black
except ImportError:
    pass

import copy
try:
    from collections import OrderedDict
except ImportError:
    print ImportError
    from ordereddict import OrderedDict


def group_reports_as_json(request):
    if (request.GET.get('group')):
        group_id = request.GET.get('group')
    else:
        group_id = "default"
    charts = _load_charts()
    data = []
    chartdata = {}
    for chart_id, chart in charts.iteritems():
        if chart.group == group_id:
            for query_id in chart.queries:
                chartdata = chart.handler(chart, query_id)
                chartdata['chart_id'] = chart_id
                chartdata['query_id'] = query_id
                data.append(chartdata)

    return HttpResponse(content=json.dumps(data), content_type="application/json")


def dispatch_group_reports(request):
    return render(request, 'reports.html')


def dispatch_xls(request, chart_id):
    '''
    Function to render reports in spreadsheet format available for download
    '''
    query_id = request.GET.get('query')
    chart_id = chart_id.split('.')[0]
    params = _augment_params(request.GET.copy(), request)
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Chart-' + chart_id)
    font_style = xlwt.easyxf('font: name Times New Roman, color-index green, bold on;align: wrap on', num_format_str='#,##0.00')
    charts = _load_charts()
    for key, value in charts.iteritems():

        if chart_id is not None and key == chart_id:
            cols = map(lambda c: c.asdict(), value.columns)
            for col in cols:
                ws.col(indexOf(cols, col)).width = int(13 * 260)

            with connections[value.database].cursor() as cursor:
                cursor.execute(value.queries[query_id], params)
                for desc in cursor.description:
                    ws.write(0, indexOf(cursor.description, desc), desc[0], font_style)

                for db_row in cursor:
                    for col_index, chart_col in enumerate(cols):
                        value = db_row[col_index]
                        value = _convert_to_type(value, chart_col['type'])
                        ws.write(indexOf(cursor, db_row) + 1, col_index, value)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xls'
    wb.save(response)
    return response


def dispatch_pdf(request, chart_id):
    '''Function to render reports in pdf format available for download'''
    query_id = request.GET.get('query')
    chart_id = chart_id.split('.')[0]
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Report.pdf'

    params = _augment_params(request.GET.copy(),request)
    p = canvas.Canvas(response)
    p.setFont("Times-Roman", 14)
    charts = _load_charts()
    for key, value in charts.iteritems():
        cols = map(lambda c: c.asdict(), value.columns)

        with connections[value.database].cursor() as cursor:
            cursor.execute(value.queries[query_id], params)
            p.setFillColor(green)
            for desc in cursor.description:
                p.drawString(indexOf(cursor.description, desc) * 2 * inch + 1 * inch, 10.5 * inch, desc[0])
            row_count = 0
            p.setFillColor(black)
            p.setFont("Times-Roman", 12)
            for db_row in cursor:
                row_count += 1
                if row_count >= 20:
                    row_count = 0
                    p.showPage()
                    p.setFillColor(black)
                    p.setFont("Times-Roman", 12)

                for col_index, chart_col in enumerate(cursor.description):
                    value = db_row[col_index]
                    value = value
                    p.drawString(col_index * 2 * inch + 1 * inch, ((11 * inch) - row_count * 0.5 * inch - 0.5 * inch), str(value))

    p.showPage()
    p.save()

    return response


def dispatch_chart(request, chart_id):
    """
    This view renders the chart data in desirable format to the controller
    """
    query_id = request.GET.get('query')
    chart_id = chart_id.split('.')[0]
    params = _augment_params(request.GET.copy(), request)
    data = []
    charts = _load_charts()
    for key, value in charts.iteritems():
        if key == chart_id:
            data.append(value.handler(value, query_id, params))
    return HttpResponse(content=json.dumps(data), content_type="application/json")


def index(request):
    return render(request, 'index.html')


def report(chart, query_id, params=None):
    data = {}
    data['rows'] = rows = []
    data['cols'] = cols = []
    data['chart_type'] = 'Table'
    with connections[chart.database].cursor() as cursor:
        cursor.execute(chart.queries[query_id], params)
        for desc in cursor.description:
            cols.append({'type':'string', 'label':desc[0]})

        for db_row in cursor:
            row_list = []
            for col_index, chart_col in enumerate(cols):
                value = db_row[col_index]
                temp = {"v": str(value)}
                row_list.append(temp)
            rows.append({"c": row_list})
    return data


def multiple_series_row(chart, query_id, params=None):

    """
    Handles the multiple series data when the series name are
    to be extracted from the rows of query set
    """

    data = {}
    data['cols'] = cols = []
    data['rows'] = rows = []
    data['chart_type'] = chart.chart_type
    type_dict = {}
    for column in chart.columns:
        type_dict[column.id] = column.type
    with connections[chart.database].cursor() as cursor:
        cursor.execute(chart.queries[query_id], params)

#TODO: Variable names are not good
#Check if result set is empty will this still work
        first_column = []
        second_column = []
        temp_val = []
        first_column_type = cursor.description[0][0]
        second_column_type = cursor.description[1][0]
        for db_row in cursor:

            if db_row[0] not in first_column:
                first_column.append(db_row[0])
                rows.append({"c": [{"v":  _convert_to_type(db_row[0], type_dict[first_column_type])}]})
            if db_row[1] not in second_column:
                second_column.append(db_row[1])
                temp_val.append({"v": _fill_missing_values(type_dict[second_column_type])})

        for row in rows:
            row['c'].extend(copy.deepcopy(temp_val))

        for db_row in cursor:
            for row in rows:
                if row['c'][0]['v'] == _convert_to_type(db_row[0], type_dict[first_column_type]):
                    index = 1 + second_column.index(db_row[1])
                    rows[indexOf(rows, row)]['c'][index]['v'] = _convert_to_type(db_row[2], type_dict[second_column_type])

        cols.append({"id": chart.columns[0].id, "type": chart.columns[0].type, "label": chart.columns[0].label})

        for series in second_column:
            cols.append({"id": series, "type": chart.columns[1].type, "label": series})

    return data


def default_handler(chart, query_id, params=None):
    """
    Handles the multiple series chart when the table has series name as
    one of the columns
    """
    data = {}
    data['rows'] = rows = []
    data['cols'] = cols = map(lambda c: c.asdict(), chart.columns)
    data['chart_type'] = chart.chart_type

    with connections[chart.database].cursor() as cursor:

        cursor.execute(chart.queries[query_id], params)
        for db_row in cursor:

            row_list = []
            for col_index, chart_col in enumerate(cols):
                value = db_row[col_index]
                value = _convert_to_type(value, chart_col['type'])
                temp = {"v": value}
                row_list.append(temp)
            rows.append({"c": row_list})

    return data


def _fill_missing_values(data_type):
    if data_type == "string":
        return ""
    elif data_type == "number":
        return 0


def _convert_to_type(value, type_desired):

    if type_desired == 'string':
        if not value:
            return None
        if isinstance(value, basestring):
            return value
        elif isinstance(value, (date, datetime)):
            return "%s.0" % str(value)
        else:
            return str(value)
    elif type_desired == 'number':
        return _coerce_number(value)
    elif type_desired == 'timeofday':
        return _to_time_of_day(value)
    elif type_desired == 'date':
        value = 'Date(' + str(value.year) + ', ' + str(value.month) + ', ' + str(value.day) + ')'
        return value
    assert False, "Invalid column type %s" % type_desired


def _coerce_number(possibly_number, default=0):
    if isinstance(possibly_number, Decimal):
        return str(possibly_number)
    if isinstance(possibly_number, (int, float)):
        return possibly_number
    try:
        if isinstance(possibly_number, basestring):
            return float(possibly_number.strip())
        else:
            return int(possibly_number)
    except:
        return default


def _to_time_of_day(str_or_int):
    if isinstance(str_or_int, int):
        seconds = str_or_int
        minutes = seconds / 60
        seconds = seconds % 60
        hours = minutes / 60
        minutes = minutes % 60
        return (hours, minutes, seconds, 0)
    elif isinstance(str_or_int, float):
        seconds = str_or_int
        minutes = seconds / 60
        seconds = seconds % 60
        hours = minutes / 60
        minutes = minutes % 60
        return (hours, minutes, seconds, 0)
    elif isinstance(str_or_int, basestring):
        tokens = str_or_int.split(":")
        if len(tokens) > 1:
            hour = _coerce_number(tokens[0], 0)
            minute = _coerce_number(tokens[1], 0)
            return (hour, minute, 0, 0)
        else:
            return (0, 0, 0, 0)
    else:
        assert False


class Column(object):
    '''Represents a <column> from charts.xml'''

    column_types = ['string', 'number', 'timeofday', 'date']

    def __init__(self, col_id, label, col_type):
        assert ' ' not in col_id, '''column id must not
                        contain a space (%s, %s)''' % (col_id, label)
        assert col_type in Column.column_types, 'Unsupported column type %s' % col_type
        self.id = col_id
        self.label = label
        self.type = col_type

    def asdict(self):
        return {"id": self.id, "label": self.label, "type": self.type}


class ChartData(object):
    '''Represents a <chart> from charts.xml

        chart_handler is a function that handles generating chart data
        into an object that the client can understand.
        chart_handler must take the following parameters :
           1. The chart object
           2. A dictionary containing query parameters
        The method is expected to be defined in the module
    '''

    owner_types = ['lineOfBusiness', 'source']

    def __init__(self, chart_id, database, group, chart_handler, queries, columns, chart_type):

        self.id = chart_id
        self.database = database
        self.handler = globals()[chart_handler]
        self.queries = queries
        self.chart_type = chart_type
        self.group = group
        if columns:
            self.columns = tuple(columns)
        else:
            self.columns = ()


def _parse_charts(charts_xml):
    doc = ET.parse(charts_xml)
    parsed_charts = OrderedDict()
    charts = doc.findall("chart")
    for chart in charts:
        chart_id = chart.get("id")
        if chart.get("database"):
            db = chart.get("database")
        else:
            db = 'default'
        if chart.get("group"):
            group = chart.get("group")
        else:
            group = 'default'

        if chart.find("handler") is not None:
            chart_handler = chart.find("handler").text
        else:
            chart_handler = "default_handler"
        current_queries = {}
        current_columns = []
        if chart.find("columns") is not None:
            columns = chart.find("columns").findall("column")
            for c in columns:
                col_id = c.find("id").text
                label = c.find("label").text
                col_type = c.find("type").text
                column = Column(col_id, label, col_type)
                current_columns.append(column)

        queries = chart.find("queries").findall("query")
        for query in queries:
            query_id = query.get("id")
            sql = query.text
            current_queries[query_id] = sql
        if chart.find("type") is not None:
            chart_type = chart.find("type").text
        else:
            chart_type = "Table"
        current_chart = ChartData(chart_id, db, group, chart_handler, current_queries, current_columns, chart_type)
        parsed_charts[chart_id] = current_chart
    return parsed_charts


def _augment_params(params, request):
    processors = []
    if 'parameter_processors' in settings.HIDASH_SETTINGS:
        processors = settings.HIDASH_SETTINGS['parameter_processors']

    for processor in processors:
        params = processor(params, request)
    return params


def _load_charts():
    # Assumes charts.xml is present in the same directory as this python file
    # charts_dir = split(abspath(__file__))[0]
    # charts_xml = join(charts_dir, "charts.xml")

    if 'xml_file_path' in settings.HIDASH_SETTINGS:
        charts_xml = settings.HIDASH_SETTINGS['xml_file_path']
    else:
        return None

    return _parse_charts(charts_xml)