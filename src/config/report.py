from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime
import weasyprint
from django.conf import settings


class GeneratePDF:
    def render_to_pdf(self, query, template, style, name):
        template = get_template(template)
        html  = template.render(query)
        result = BytesIO()
        print(result)
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
        if not pdf.err:
            filename = f'{datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")}{name}.pdf'
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            weasyprint.HTML(string=html).write_pdf(response, 
                    stylesheets=[
                        weasyprint.CSS(f"{settings.STATICFILES_DIRS[0]}{style}"),
                    ])
            return response
        return HttpResponse("Not found")
        

        