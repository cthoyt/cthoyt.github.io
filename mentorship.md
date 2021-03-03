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
    {{ entry.name }}
    {% if entry contains "orcid" %}
        <a href="https://orcid.org/{{ entry.orcid }}">
        <img alt="ORCID logo" src="https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png" width="16" height="16" />
        </a>
    {% endif %}
    {% if entry contains "linkedin" %}
        <a href="https://linkedin.com/in/{{ entry.linkedin }}">
        <img alt="LinkedIn logo" src="/img/logos/linkedin-icon.svg" width="16" height="16" />
        </a>
    {% endif %}
    {% if entry contains "github" %}
        <a href="https://github.com/in/{{ entry.github }}">
        <img alt="GitHub logo" src="/img/logos/github-icon.svg" width="16" height="16" />
        </a>
    {% endif %}
    <ul>
        {% for role in entry.roles %}
        <li>
        {{ role.name }}{% if role.location.group.name %} in the
        {% if role.location.group.url %}
        <a href="{{ role.location.group.url }}">{{ role.location.group.name }}</a> 
        {% else %}
        {{ role.location.group.name }}
        {% endif %}{% endif %}
        in the {{ role.location.organization.name }}
        {% if role.location.institute.url %}
        <a href="{{ role.location.institute.url }}">{{ role.location.institute.name }}</a>
        {% else %}
        {{ role.location.institute.name }}
        {% endif %}
        {% if role.end %}
        from {{ role.start.month }}
        {% if role.start.year != role.end.year %}
            {{ role.start.year }}
        {% endif %}
        to {{ role.end.month }} {{ role.end.year }}
        {% else %}
        starting {{ role.start.month }} {{ role.start.year }}
        {% endif %}
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
    {{ entry.name }}
    {% if entry contains "orcid" %}
        <a href="https://orcid.org/{{ entry.orcid }}">
        <img alt="ORCID logo" src="https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png" width="16" height="16" />
        </a>
    {% endif %}
    {% if entry contains "linkedin" %}
        <a href="https://linkedin.com/in/{{ entry.linkedin }}">
        <img alt="LinkedIn logo" src="/img/logos/linkedin-icon.svg" width="16" height="16" />
        </a>
    {% endif %}
    {% if entry contains "github" %}
        <a href="https://github.com/in/{{ entry.github }}">
        <img alt="GitHub logo" src="/img/logos/github-icon.svg" width="16" height="16" />
        </a>
    {% endif %}
    <ul>
        {% for role in entry.roles %}
        <li>
        {{ role.name }}
        {% if role.location.group.name %}
        in the
        <a href="{{ role.location.group.url }}">{{ role.location.group.name }}</a>
        {% endif %}
        in the {{ role.location.organization.name }}
        <a href="{{ role.location.institute.url }}">{{ role.location.institute.name }}</a>
        from {{ role.start.month }}
        {% if role.start.year != role.end.year %}
            {{ role.start.year }}
        {% endif %}
        {% if role.end %}
        to {{ role.end.month }} {{ role.end.year }}
        {% else %}
        (current)
        {% endif %}
        </li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>
