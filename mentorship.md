---
layout: page
title: Mentorship
permalink: /mentorship/
---

## My Mentors

<ul>
{% for entry in site.data.mentors %}
    <li>
    {% if entry contains "orcid" %}
    <img src="https://orcid.org/sites/default/files/images/orcid_16x16(1).gif" alt="ORCID"/>
    <a href="https://orcid.org/{{ entry.orcid }}">{{ entry.name }}</a>
    {% else %}
    <a href="https://linkedin.com/in/{{ entry.linkedin }}">{{ entry.name }}</a>
    {% endif %}
    <ul>
        {% for role in entry.roles %}
        <li>
        {{ role.name }} at {{ role.location }} from {{ role.start }} to {{ role.end }}
        </li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>

## My Mentees

During my master's and doctoral work at the Fraunhofer SCAI Department of
Bioinformatics from 2016-2019, I had the opportunity to recruit, mentor, and
work with many wonderful students:

<ul>
{% for entry in site.data.mentees %}
    <li>
    {% if entry contains "orcid" %}
    <img src="https://orcid.org/sites/default/files/images/orcid_16x16(1).gif" alt="ORCID"/>
    <a href="https://orcid.org/{{ entry.orcid }}">{{ entry.name }}</a>
    {% else %}
    {{ entry.name }}
    {% endif %}
    <ul>
        {% for role in entry.roles %}
        <li>
        {{ role.name }} at {{ role.location }} from {{ role.start }} to {{ role.end }}
        </li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>
