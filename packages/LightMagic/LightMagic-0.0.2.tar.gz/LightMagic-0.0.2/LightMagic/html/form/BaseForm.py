class BaseForm:
    """Базовый класс для форм"""

    def __init__(self, name, value=None, prefix=None, placeholder=None, attributes=None, **kwargs):
        """Конструктор"""
        self._name = name
        self._value = value
        self._prefix = prefix
        self._placeholder = placeholder
        self._attributes = attributes

        # Устанавливаем дополнительные аттрибуты
        for item in kwargs:
            setattr(self, '_%s' % item, kwargs[item])

        # # Забрать из настроек
        # self._default_value = self._cls.__dict__[self._key].value

    def render(self):
        """Отрисовывает форму"""
        raise PermissionError('Данный метод необходимо переопределить')

    def _get_attributes(self):
        """Возвращает дополнительные аргументы (настройки стиля и т.д.)"""
        if self._attributes is None:
            return ''

        attributes = []
        for key in self._attributes:
            attributes.append('%s="%s"' % (key, self._attributes[key]))
            return ' '.join(attributes)
