# coding=utf-8

from os import path
import random
from jinja2 import Environment


def datetimeformat(value, format='%d/%m/%Y %H:%M'):
    """
    Jinja filter used to format date
    :param value:
    :param format:
    :return:
    """
    return value.strftime(format)

JINJA_ENV = Environment()
JINJA_ENV.filters['datetimeformat'] = datetimeformat


class TicketRenderer(object):

    def __init__(self, ticket_template, media_url, css_url):
        """
        :param ticket_template: a ticket template used to configure a photobooth
        :param media_url: base url to fetch images
        :param css_url: url to find css files
        :return:
        """
        self.template = ticket_template
        self.media_url = media_url
        self.css_url = css_url

    def render(self, picture, code, date):

        context = {
            'title': self.template['title'],
            'description': self.template['description'],
            'picture': picture,
            'datetime': date,
            'code': code,
            'css_url': self.css_url
        }

        for image in self.template['images']:
            image_url = self.get_image_url(image['name'])
            context['image_%s' % image['id']] = image_url

        for image_variable in self.template['image_variables']:
            if image_variable['items']:
                choice = random.choice(image_variable['items'])
                uid = 'imagevariable_%s' % image_variable['id']
                context[uid] = self.get_image_url(choice['name'])

        for text_variable in self.template['text_variables']:
            if text_variable['items']:
                choice = random.choice(text_variable['items'])
                uid = 'textvariable_%s' % text_variable['id']
                context[uid] = choice['text']

        template = JINJA_ENV.from_string(self.template['html'])
        return template.render(context)

    def get_image_url(self, image_name):
        return path.join(self.media_url, 'images', image_name)