---
layout: page
title: Teaching
permalink: /teaching/
---
## Courses

<ul>
{% for entry in site.data.courses %}
    <li>
    <i>{{ entry.name }}</i> at {{ entry.university }} during {{ entry.period }}
    ({{ entry.level }} - {{ entry.type }} as a ({{ entry.role }})
    </li>
{% endfor %}
</ul>

## Academic Lectures

<ul>
{% for entry in site.data.lectures %}
    <li>
    <a href="{{ entry.url }}">{{ entry.name }}</a>
    for {{ entry.course }} at {{ entry.department }} at {{ entry.university }} during {{ entry.period }}
    </li>
{% endfor %}
</ul>

## Invited Lectures

<ul>
{% for entry in site.data.lectures %}
    <li>
    <a href="{{ entry.url }}">{{ entry.name }}</a>
    for {{ entry.venue }} at {{ entry.location }} on {{ entry.date }}
    </li>
{% endfor %}
</ul>
