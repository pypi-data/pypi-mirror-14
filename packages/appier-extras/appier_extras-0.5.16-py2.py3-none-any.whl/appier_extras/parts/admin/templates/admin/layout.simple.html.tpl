{% extends "admin/layout.base.html.tpl" %}
{% block html %}
    {% include "admin/doctype.html.tpl" %}
    <head>
        {% block head %}
            {% include "admin/content_type.html.tpl" %}
            {% include "admin/includes.html.tpl" %}
            <title>{% block htitle %}{% endblock %}</title>
        {% endblock %}
    </head>
    <body class="ux wait-load simple {{ sub_layout_r }} {{ style_r }} {{ style_flags }}" data-id="admin">
        <div id="overlay" class="overlay"></div>
        <div id="header" class="header">
            {% block header %}
                {% include "admin/header.html.tpl" %}
            {% endblock %}
        </div>
        <div id="content" class="content {% block style %}{% endblock %}">{% block content %}{% endblock %}</div>
        <div id="footer" class="footer">
            {% block footer %}
                {% include "admin/footer.html.tpl" %}
            {% endblock %}
        </div>
    </body>
    {% include "admin/end_doctype.html.tpl" %}
{% endblock %}
