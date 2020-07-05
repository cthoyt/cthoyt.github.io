---
layout: page
title: Software
permalink: /software/
---
I've worked on several open source projects, and still do quite a bit of maintenance on them:

<ul>
{% for entry in site.data.software %}
    <li>
    {% if entry contains "logo" %}
    <img src="{{ entry.logo }}" alt="{{ entry.name }} Logo" style="float: right; max-height: 40px; max-width: 40px;" />
    {% endif %}
    <strong><a href="https://github.com/{{ entry.github }}">{{ entry.name }}</a></strong>
    {{ entry.description }} ({{ entry.role }})
    </li>
{% endfor %}
</ul>
