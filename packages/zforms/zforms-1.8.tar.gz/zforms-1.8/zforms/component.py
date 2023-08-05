from flask import render_template, request, flash
from markupsafe import Markup
from zforms.validators import ValidationException
import itertools

class FormException(Exception):
	def __init__(self, errors=list()):
		self.errors = errors

	def flash(self, messageFormat='{name} - {message}', category='error'):
		for (name, error) in self.errors:
			flash(messageFormat.format(name=name, message=error), category)

class FormRenderException(Exception):
	pass

class FormComponentException(Exception):
	def __init__(self, name, errors=list()):
		self.name = name
		self.errors = errors

POST_INPUT, GET_INPUT, FILE_INPUT = range(3)

class FormComponent(object):
	def __init__(self, name, template=None, ftype=POST_INPUT, validators=list(), required=True, isList=False, **templateData):
		self.name = name
		self.template = template
		self.ftype = ftype
		self.validators = validators
		self.required = required
		self.isList = isList
		self.templateData = templateData


	def validate(self):
		errors = []
		if self.ftype == POST_INPUT:
			requestData = request.form
		elif self.ftype == FILE_INPUT:
			requestData = request.files
		elif self.ftype == GET_INPUT:
			requestData = request.args
		else:
			errors.append('Form type invalid.')
			raise FormComponentException(self.name, errors)

		if not self.isList:
			data = requestData.get(self.name, None)
		else:
			data = requestData.getlist(self.name)

		if data is None or (self.isList and len(data) == 0):
			if self.required:
				errors.append('Form data not sent.')
				raise FormComponentException(self.name, errors)
			return True

		for validator in self.validators:
			try:
				data = validator(data)
			except ValidationException as ex:
				errors.append(ex.message)

		if len(errors) == 0:
			return data
		raise FormComponentException(self.name, errors)

	@property
	def canRender(self):
		return self.template is not None

	def render(self):
		if not self.canRender:
			raise FormRenderException()
		return Markup(render_template(self.template, **self.templateData))

class Form(object):
	def __init__(self, components, template=None, **templateData):
		self.components = components
		self.template = template
		self.templateData = templateData

	def validate(self):
		result = dict()
		errors = []
		for component in self.components:
			try:
				result[component.name] = component.validate()
			except FormComponentException as ex:
				for error in ex.errors:
					errors.append((ex.name, error))
		if len(errors) > 0:
			raise FormException(errors)
		return result

	@property
	def canRender(self):
		return self.template is not None and all(itertools.imap(lambda x: x.canRender, self.components))

	def render(self):
		if not self.canRender:
			raise FormRenderException()
		return Markup(render_template(self.template, components=self.components, **self.templateData))