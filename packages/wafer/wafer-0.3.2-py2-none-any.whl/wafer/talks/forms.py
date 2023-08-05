from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from markitup.widgets import MarkItUpWidget
from easy_select2.widgets import Select2Multiple

from wafer.talks.models import Talk, render_author


class TalkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TalkForm, self).__init__(*args, **kwargs)

        if not self.user.has_perm('talks.edit_private_notes'):
            self.fields.pop('private_notes')

        # We add the name, if known, to the authors list
        self.fields['authors'].label_from_instance = render_author

        self.helper = FormHelper(self)
        submit_button = Submit('submit', _('Submit'))
        instance = kwargs['instance']
        if instance:
            self.helper.layout.append(
                FormActions(
                    submit_button,
                    HTML('<a href="%s" class="btn btn-danger">%s</a>'
                         % (reverse('wafer_talk_delete', args=(instance.pk,)),
                            _('Delete')))))
        else:
            self.helper.add_input(submit_button)

    class Meta:
        model = Talk
        fields = ('title', 'talk_type', 'abstract', 'authors', 'notes',
                  'private_notes')
        widgets = {
            'abstract': MarkItUpWidget(),
            'notes': forms.Textarea(attrs={'class': 'input-xxlarge'}),
            'authors': Select2Multiple(),
        }

# TODO: authors widget is ugly
