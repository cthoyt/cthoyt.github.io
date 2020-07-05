---
layout: page
title: Software
permalink: /software/
---
I've worked on several open source projects, and still do quite a bit of maintenance on them

<ul>
{% for entry in site.data.software %}
    <li>
    <a href="https://github.com/{{ entry.github }}">{{ entry.name }}</a>
    {{ entry.description }} ({{ entry.role }})
    </li>
{% endfor %}
</ul>
