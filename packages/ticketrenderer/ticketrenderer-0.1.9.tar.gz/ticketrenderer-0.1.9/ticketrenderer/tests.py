import unittest
from datetime import datetime

from .ticketrenderer import TicketRenderer


class TestTicketRenderer(unittest.TestCase):

    def setUp(self):
        self.media_url = 'http://media/'
        self.css_url = 'http://static/ticket.css'

    def test_render(self):
        """
        TicketRenderer should render a ticket
        """

        html = '{{css_url}} {{picture}} {{code}} {{datetime | datetimeformat}} ' \
               '{{textvariable_1}} {{imagevariable_2}} ' \
               '{{image_3}}'
        texts = [{'text':'Titi'}, {'text':'Vicky'}, {'text':'Benni'}]
        text_variables = [{'id': '1', 'items': texts}]

        items = [
            {
                'id': '1',
                'name': 'image1'

            },
            {
                'id': '2',
                'name': 'image2'
            }
        ]
        image_variables = [{'id': '2', 'items': items}]
        images = [{'id': '3', 'name': 'image3'}]
        template = {
            'html': html,
            'images': images,
            'image_variables': image_variables,
            'text_variables': text_variables,
            'title': 'title',
            'description': 'description'
        }
        ticket_renderer = TicketRenderer(template, self.media_url, self.css_url)
        code = 'SJ98H'
        date = datetime(2016, 01, 01)
        picture = 'http://path/to/picture'
        rendered = ticket_renderer.render(code=code, date=date, picture=picture)
        self.assertIn("http://path/to/picture", rendered)
        self.assertIn(code, rendered)
        self.assertIn("http://static/ticket.css", rendered)
        self.assertTrue("Titi" in rendered or "Vicky" in rendered or "Benni" in rendered)
        self.assertTrue("http://media/images/image1" in rendered or "http://media/images/image2" in rendered)
        self.assertTrue("http://media/images/image3" in rendered)
        self.assertIn("01/01/2016 00:00", rendered)

    def test_render_no_variables_no_title_no_description(self):
        """
         Ticket renderer should render even if no variables, nor title, nor description are set
        """
        html = '{{css_url}} {{picture}} {{code}} {{datetime | datetimeformat}}'
        template = {
            'html': html,
            'images': [],
            'image_variables': [],
            'text_variables': [],
            'title': None,
            'description': None
        }
        ticket_renderer = TicketRenderer(template, self.media_url, self.css_url)
        code = 'SJ98H'
        date = datetime(2016, 01, 01)
        picture = 'http://path/to/picture'
        rendered = ticket_renderer.render(code=code, date=date, picture=picture)
        self.assertIn("http://path/to/picture", rendered)
        self.assertIn(code, rendered)
        self.assertIn("http://static/ticket.css", rendered)


    def test_render_no_items_in_variable(self):
        """
        Ticket renderer should render a template with a variable that have no items
        """
        html = '{{css_url}} {{picture}} {{code}} {{datetime | datetimeformat}} {{textvariable_1}}'
        text_variables = [{'id': '1', 'items': []}]
        template = {
            'html': html,
            'images': [],
            'image_variables': [],
            'text_variables': text_variables,
            'title': 'title',
            'description': 'description'
        }
        ticket_renderer = TicketRenderer(template, self.media_url, self.css_url)
        code = 'SJ98H'
        date = datetime(2016, 01, 01)
        picture = 'http://path/to/picture'
        rendered = ticket_renderer.render(code=code, date=date, picture=picture)
        self.assertIn("http://path/to/picture", rendered)
        self.assertIn(code, rendered)
        self.assertIn("http://static/ticket.css", rendered)

    def test_set_date_format(self):
        """
        Ticket renderer should handle datetimeformat filter
        """
        html = '{{datetime | datetimeformat("%Y/%m/%d")}}'
        template = {
            'html': html,
            'images': [],
            'image_variables': [],
            'text_variables': [],
            'title': '',
            'description': ''
        }
        ticket_renderer = TicketRenderer(template, self.media_url, self.css_url)
        code = 'SJ98H'
        date = datetime(2010, 01, 01)
        picture = 'http://path/to/picture'
        rendered_html = ticket_renderer.render(code=code, date=date, picture=picture)
        assert "2010/01/01" in rendered_html


    def test_encode_non_unicode_character(self):
        """
        Ticket renderer should encode non unicode character
        """
        html = u"Du texte avec un accent ici: é"
        template = {
            'html': html,
            'images': [],
            'image_variables': [],
            'text_variables': [],
            'title': '',
            'description': ''
        }
        ticket_renderer = TicketRenderer(template, self.media_url, self.css_url)
        code = 'SJ98H'
        date = datetime(2010, 01, 01)
        picture = 'http://path/to/picture'
        rendered_html = ticket_renderer.render(code=code, date=date, picture=picture)
        assert u'Du texte avec un accent ici: é' in rendered_html


if __name__ == '__main__':
    unittest.main()




