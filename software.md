---
layout: page
title: Software
permalink: /software/
---
I've worked on several open source projects, and still do quite a bit of maintenance on them

<dl>
{% for entry in site.data.software %}
    <dt><a href="https://github.com/{{ entry.github }}">{{ entry.name }}</a></dt>
    <dd>{{ entry.description }} ({{ entry.role }})</dd>
{% endfor %}
</dl>
