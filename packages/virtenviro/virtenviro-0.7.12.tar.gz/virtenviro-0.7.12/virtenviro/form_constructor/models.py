#~*~ coding: utf-8 ~*~
from django.db import models
from django.utils.translation import ugettext_lazy as _

ENCTYPES = (
    ('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded'),
    ('multipart/form-data', 'multipart/form-data'),
    ('text/plain', 'text/plain')
)
METHODS = (
    ('GET', 'GET'),
    ('POST', 'POST')
)
TARGETS = (
    ('_blank', '_blank'),
    ('_self', '_self'),
    ('_parent', '_parent'),
    ('_top', '_top')
)


class Form(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    action = models.CharField(max_length=5000, verbose_name=_('Action'), null=True, blank=True)
    enctype = models.CharField(max_length=40, verbose_name=_('Enctype'), default='application/x-www-form-urlencoded',
                               choices=ENCTYPES)
    method = models.CharField(max_length=4, verbose_name=_('Method'),
                              help_text=_('Data transfer method'),
                              choices=METHODS, default='GET')
    novalidate = models.BooleanField(default=False, verbose_name=_('Do not validate'))
    target = models.CharField(max_length=7, verbose_name=_('Target'), choices=TARGETS, null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')


class Field(models.Model):
    TAGS = (
        ('input', 'input'),
        ('textarea', 'textarea'),
        ('button', 'button'),
    )
    ALIGNS = (
        ('bottom', _('bottom')),
        ('left', _('left')),
        ('middle', _('middle')),
        ('right', _('right')),
        ('top', _('top')),
    )
    TYPES = (
        ('text', 'text'),
        ('button', 'button'),
        ('checkbox', 'checkbox'),
        ('file', 'file'),
        ('hidden', 'hidden'),
        ('hidden', 'hidden'),
        ('image', 'image'),
        ('password', 'password'),
        ('radio', 'radio'),
        ('reset', 'reset'),
        ('submit', 'submit'),
        ('textarea', 'textarea'),
        ('email', 'email'),
        ('number', 'number'),
        ('range', 'range'),
        ('search', 'search'),
        ('tel', 'tel'),
        ('url', 'url'),
    )
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    form = models.ForeignKey(Form, verbose_name=_('Form'))
    value = models.TextField(verbose_name=_('Default value'), )

    in_form = models.BooleanField(default=True, verbose_name=_('Is input in form?'))
    field_tag = models.CharField(max_length=10, verbose_name=_('Field tag'), default='input', choices=TAGS)
    field_type = models.CharField(max_length=200, verbose_name=_('Type'), choices=TYPES, default='text')
    align = models.CharField(max_length=6, verbose_name=_('Align'),
                             help_text=_('Image input alignment'), choices=ALIGNS, null=True, blank=True)
    alt = models.CharField(max_length=255, verbose_name=_('Image alt text'))
    autofocus = models.BooleanField(verbose_name=_('Auto focus'), default=False)
    border = models.IntegerField(verbose_name=_('Image input border'), null=True, blank=True)
    chacked = models.BooleanField(verbose_name=_('Checked'), default=False)
    disabled = models.BooleanField(verbose_name=_('Disabled'), default=False)

    formaction = models.CharField(max_length=5000, verbose_name=_('Action'), null=True, blank=True)
    formenctype = models.CharField(max_length=40, verbose_name=_('Enctype'), default='application/x-www-form-urlencoded',
                               choices=ENCTYPES, null=True, blank=True)
    formmethod = models.CharField(max_length=4, verbose_name=_('Method'),
                              help_text=_('Data transfer method'),
                              choices=METHODS, default='GET', null=True, blank=True)
    formnovalidate = models.BooleanField(default=False, verbose_name=_('Do not validate'))
    formtarget = models.CharField(max_length=7, verbose_name=_('Target'), choices=TARGETS, null=True, blank=True)

    datalist = models.TextField(verbose_name=_('List'), null=True, blank=True)
    maxlength = models.IntegerField(verbose_name=_('Max length'), null=True, blank=True)
    max_val = models.IntegerField(verbose_name=_('Max value'), default=0)
    min_val = models.IntegerField(verbose_name=_('Min value'), default=0)
    step = models.IntegerField(verbose_name=_('Step'), default=0)

    multiple = models.BooleanField(default=False, verbose_name=_('Multiple file upload'))
    pattern = models.CharField(max_length=255, verbose_name=_('Pattern'), null=True, blank=True)
    placeholder = models.CharField(max_length=255, verbose_name=_('Placeholder'), null=True, blank=True)
    required = models.BooleanField(default=False, verbose_name=_('Required'))

    styles = models.CharField(max_length=255, verbose_name=_('Styles'), null=True, blank=True)
    ordering = models.IntegerField(default=999, verbose_name=_('Ordering'))

    def clean(self):
        if not self.field_type == 'image':
            self.align = None
            self.alt = None
        if not self.field_type == 'checkbox':
            self.chacked = False

        if not self.min_val and self.max_val < self.min_val:
            self.max_val = self.min_val

    '''
    accept Устанавливает фильтр на типы файлов, которые вы можете отправить через поле загрузки файлов.
    align Определяет выравнивание изображения.
    alt Альтернативный текст для кнопки с изображением.
    autofocus Устанавливает фокус в поле формы.
    border Толщина рамки вокруг изображения.
    checked Предварительно активированный переключатель или флажок.
    disabled Блокирует доступ и изменение элемента.

    form Связывает поле с формой по её идентификатору.
    formaction Определяет адрес обработчика формы.
    formenctype Устанавливает способ кодирования данных формы при их отправке на сервер.
    formmethod Сообщает браузеру каким методом следует передавать данные формы на сервер.
    formnovalidate Отменяет встроенную проверку данных на корректность.
    formtarget Определяет окно или фрейм в которое будет загружаться результат, возвращаемый обработчиком формы.

    list Указывает на список вариантов, которые можно выбирать при вводе текста.
    max Верхнее значение для ввода числа или даты.
    maxlength Максимальное количество символов разрешенных в тексте.
    min Нижнее значение для ввода числа или даты.

    multiple Позволяет загрузить несколько файлов одновременно.
    name Имя поля, предназначено для того, чтобы обработчик формы мог его идентифицировать.
    pattern Устанавливает шаблон ввода.
    placeholder Выводит подсказывающий текст.
    readonly Устанавливает, что поле не может изменяться пользователем.
    required Обязательное для заполнения поле.
    size Ширина текстового поля.
    src Адрес графического файла для поля с изображением.
    step Шаг приращения для числовых полей.
    tabindex Определяет порядок перехода между элементами с помощью клавиши Tab.
    type Сообщает браузеру, к какому типу относится элемент формы.
    value Значение элемента.
    '''

    def __unicode__(self):
        return self.title


class Action(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')
