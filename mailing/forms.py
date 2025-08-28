from django import forms
from .models import Message, Recipient, Mailing


class MailingForm(forms.ModelForm):
    """
    Форма для создания и редактирования рассылки.

    Включает выбор получателей и сообщения, доступных для текущего пользователя.
    """

    class Meta:
        model = Mailing
        fields = "__all__"
        exclude = ["owner"]
        widgets = {"recipients": forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и фильтрует получателей и сообщения по владельцу.

        Параметры:
        *args: Аргументы, переданные в родительский класс.
        **kwargs: Ключевые аргументы, переданные в родительский класс, включая пользователя.
        """
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["recipients"].queryset = Recipient.objects.filter(owner=user)
            self.fields["message"].queryset = Message.objects.filter(owner=user)


class RecipientForm(forms.ModelForm):
    """
    Форма для создания и редактирования получателя рассылки.
    """

    class Meta:
        model = Recipient
        fields = "__all__"
        exclude = ["owner"]


class MessageForm(forms.ModelForm):
    """
    Форма для создания и редактирования сообщения.
    """

    class Meta:
        model = Message
        fields = "__all__"
        exclude = ["owner"]