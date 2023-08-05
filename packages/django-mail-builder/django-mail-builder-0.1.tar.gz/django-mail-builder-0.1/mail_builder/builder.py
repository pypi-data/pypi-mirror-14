from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import select_template
from django.template.loader_tags import BlockNode


def render_block(template, block_name, context):
    for node in template.nodelist.get_nodes_by_type(BlockNode):
        if node.name == block_name:
            return node.render(context).strip()
    return None


def build_message(template_names, extra_context=None, force_multipart=False,
                  **defaults):
    if not isinstance(template_names, (list, tuple)):
        template_names = (template_names,)
    tmpl = select_template(template_names)
    tmpl = getattr(tmpl, 'template', tmpl)  # Unwrap for Django 1.8+

    if extra_context is None:
        extra_context = {}

    data = dict(defaults)
    data.setdefault('body', '')

    # Scalar values
    for field in ('subject', 'from_email', 'body', 'html'):
        value = render_block(tmpl, field, extra_context)
        if value is not None:
            data[field] = value

    # List values
    for field in ('to', 'bcc', 'cc', 'reply_to'):
        value = render_block(tmpl, field, extra_context)
        if value is not None:
            data[field] = value.splitlines()

    html_content = data.pop('html', None)
    if force_multipart or html_content:
        msg = EmailMultiAlternatives(**data)
        if html_content:
            msg.attach_alternative(html_content, 'text/html')
    else:
        msg = EmailMessage(**data)

    return msg
