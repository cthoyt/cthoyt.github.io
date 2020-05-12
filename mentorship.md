---
layout: page
title: Mentorship
permalink: /mentorship/
---
As scientists, we owe a great deal to our mentors in the classroom and lab,
each of whom altruistically invested their time and confidence in us. We can
thank them by doing the same for others, the same as they did for us.

## My Mentors

<ul>
{% for entry in site.data.mentors %}
    <li>
    {% if entry contains "orcid" %}
    <img src="https://orcid.org/sites/default/files/images/orcid_16x16(1).gif" alt="ORCID" />
    <a href="https://orcid.org/{{ entry.orcid }}">{{ entry.name }}</a>
    {% else %}
    <a href="https://linkedin.com/in/{{ entry.linkedin }}">{{ entry.name }}</a>
    {% endif %}
    <ul>
        {% for role in entry.roles %}
        <li>
        {{ role.name }} in the
        {% if role.location.group.url %}
        <a href="{{ role.location.group.url }}">{{ role.location.group.name }}</a> 
        {% else %}
        {{ role.location.group.name }}
        {% endif %}
        in the {{ role.location.organization.name }}
        {% if role.location.institute.url %}
        <a href="{{ role.location.institute.url }}">{{ role.location.institute.name }}</a>
        {% else %}
        {{ role.location.institute.name }}
        {% endif %}
        from {{ role.start.month }}
        {% if role.start.year != role.end.year %}
            {{ role.start.year }}
        {% endif %}
        to {{ role.end.month }} {{ role.end.year }}
        </li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>

## My Mentees

During my master's and doctoral work at the Fraunhofer from 2016-2019,
I had the opportunity to recruit, mentor, and work with many wonderful
students:

<ul>
{% for entry in site.data.mentees %}
    <li>
    {% if entry contains "orcid" %}
    <img src="https://orcid.org/sites/default/files/images/orcid_16x16(1).gif" alt="ORCID" />
    <a href="https://orcid.org/{{ entry.orcid }}">{{ entry.name }}</a>
    {% else %}
    {{ entry.name }}
    {% endif %}
    <ul>
        {% for role in entry.roles %}
        <li>
        {{ role.name }} in the
        <a href="{{ role.location.group.url }}">{{ role.location.group.name }}</a>
        in the {{ role.location.organization.name }}
        <a href="{{ role.location.institute.url }}">{{ role.location.institute.name }}</a>
        from {{ role.start.month }}
        {% if role.start.year != role.end.year %}
            {{ role.start.year }}
        {% endif %}
        to {{ role.end.month }} {{ role.end.year }}
        </li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>
