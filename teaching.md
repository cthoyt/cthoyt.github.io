---
layout: page
title: Teaching
permalink: /teaching/
---
I've found teaching and tutoring to be a really rewarding experience.
It has been an opportunity to improve my own knowledge and communicate
topics that I know but can't be found on the internet or in a book. 

{% for entry in site.data.courses %}
<b>{{ entry.code }} {{ entry.name }}</b> ({{ entry.period.semester }} {{ entry.period.year }}; {{ entry.role }})<br />
{{ entry.level }} at {{ entry.location.university }} ({{ entry.location.department }}){% if entry.primary %}
primarily taught by <a href="{{ entry.primary.link }}">{{ entry.primary.name }}</a>.
{% endif %}<br />

{% if entry.presentation %}
{% if entry.date %}
Guest lecture on {{ entry.date.month }} {{ entry.date.day }}, {{ entry.date.year }}:
{% elsif entry.start %}
Guest lecture series from {{ entry.start.month }} {{ entry.start.day }} - {{ entry.end.month }} {{ entry.end.day }}, {{ entry.start.year }}:
{% else %}
Guest lecture:
{% endif %} <a href="{{ entry.presentation.url }}">{{ entry.presentation.name }}</a><br />
{% if entry.presentation.description %}
<i>Description</i>: {{ entry.presentation.description }}
{% endif %}
{% endif %}
{% if entry.description %}
<i>Description</i>: {{ entry.description }}
{% endif %}
{% endfor %}

