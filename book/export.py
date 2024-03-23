import csv
from django.http import HttpResponse
from datetime import datetime


def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    today = datetime.today()
    filename = f"export_{today.strftime('%m/%d/%Y, %H:%M:')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    """
        title
        author
        department
        year_level
        year
    """

    included_fields = ['pk', 'title', 'author', 'department',
                       'year_level', 'year']  # List of field names to include
    fields = [
        field.name for field in queryset.model._meta.fields if field.name in included_fields]

    writer = csv.writer(response)

    # Write headers
    writer.writerow(fields)

    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field.name)
                        for field in obj._meta.fields if field.name in included_fields])

    return response


export_as_csv.short_description = "Export selected objects as CSV"
