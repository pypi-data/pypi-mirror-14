from django.views.generic import FormView

from .builder import build_message


class EmailFormView(FormView):
    '''
    Utility view to send email on form submission.
    '''
    email_template = None
    fail_silently = True

    def get_email_params(self):
        return {}

    def form_valid(self, form):
        msg = build_message(self.email_template,
                            extra_context={'form': form.cleaned_data},
                            **self.get_email_params())
        msg.send(fail_silently=self.fail_silently)

        return super(EmailFormView, self).form_valid(form)
