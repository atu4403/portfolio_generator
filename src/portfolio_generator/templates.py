default_template = """# {{ user }}

{%- if github %}
## github

{% for item in github %}
{%- if not item.fork and item.description %}
- [{{ item.name}}]({{ item.html_url }}): {{ item.description}} ({{ item.updated_at|to('+09:00')|fmt('YYYY-MM-DD HH:mm:ss')}})
{%- endif %}
{%- endfor %}
{%- endif %}

{%- if zenn %}
## zenn({{ zenn.entries|length }} items)

{% for item in zenn.entries %}
- [{{ item.title}}]({{ item.link }}): {{ item.published_parsed|fmt('YYYY-MM-DD HH:mm:ss')}}
{%- endfor %}
{%- endif %}

{%- if qiita %}
## qiita

{% for item in qiita %}
- [{{ item.title}}]({{ item.url }}): {{ item.created_at|fmt('YYYY-MM-DD HH:mm:ss')}}
{%- endfor %}
{%- endif %}

"""
