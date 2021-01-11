---
layout: post
title: How to Code with Me: Wrapping a Flask App in a CLI
date: 2021-01-10 00:00:00 -0800
author: Charles Tapley Hoyt
---
Previous posts in my "How to Code with Me" series have addressed
[packaging python code]({% post_url 2020-06-03-how-to-code-with-me-organization %}) and
[setting up a command line interface (CLI) using `click`]({% post_url 2020-06-11-click %}). This post is about how to
do this when your Python code is running a web application made with [Flask](https://flask.palletsprojects.com) and
how to set it up to run through your CLI.

Test
