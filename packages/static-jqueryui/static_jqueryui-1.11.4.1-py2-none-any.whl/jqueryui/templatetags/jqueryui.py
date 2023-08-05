# -*- coding: utf-8 -*-

from appconf.base import AppConf
from django import template
from django.conf import settings
from django.template.base import TextNode

from .. import __version__


register		 = template.Library()


class _AppConf(AppConf):
	VERSION				 = __version__
	CDN					 = False
	DEFAULT_CDN			 = 'http://code.jquery.com/ui/%(version)s/jquery-ui.min.js'
	THEME				 = 'redmond'
	THEME_CDN			 = False
	THEME_DEFAULT_CDN	 = 'http://code.jquery.com/ui/%(version)s/themes/%(theme)s/jquery-ui.min.css'

	STATIC_JS			 = '%(static_url)sjquery/ui/%(version)s/jquery-ui.min.js'
	STATIC_CSS			 = '%(static_url)sjquery/ui/%(version)s/themes/%(theme)s/jquery-ui.min.css'
	STATIC_CUSTOM_CSS	 = '%(static_url)sjquery/ui/%(version)s/jquery-ui.min.css'

	SCRIPT_TAG			 = '<script type="text/javascript" src="%(url)s"></script>'
	LINK_TAG			 = '<link rel="stylesheet" type="text/css" href="%(url)s" />'

	class Meta:
		prefix			 = "JQUERYUI"  # appconf cannot determine the prefix here!



@register.tag
def jqueryui_js(parser, token):
	bits	 = tuple(token.split_contents()) + (None, None)
	version	 = bits[1] or settings.JQUERYUI_VERSION
	cdn		 = settings.JQUERYUI_CDN
	if cdn:
		if cdn is True:
			cdn = settings.JQUERYUI_DEFAULT_CDN
		url	 = cdn % {'version': version}
	else:
		url	 = settings.JQUERYUI_STATIC_JS % {
			'static_url': settings.STATIC_URL, 'version': version}

	res	 = settings.JQUERYUI_SCRIPT_TAG % {'url': url}
	return TextNode(res)


@register.tag
def jqueryui_css(parser, token):
	bits	 = tuple(token.split_contents()) + (None, None)
	version	 = bits[1] or settings.JQUERYUI_VERSION
	theme	 = bits[2]
	custom_theme = version.endswith('custom') > 0 and theme is None
	theme	 = theme or settings.JQUERYUI_THEME

	cdn		 = settings.JQUERYUI_THEME_CDN
	if cdn:
		if cdn is True:
			cdn = settings.JQUERYUI_THEME_DEFAULT_CDN
		url	 = cdn % {'version': version, 'theme': theme}
	else:
		if custom_theme:
			url	 = settings.JQUERYUI_STATIC_CUSTOM_CSS % {
				'static_url': settings.STATIC_URL, 'version': version}
		else:
			url	 = settings.JQUERYUI_STATIC_CSS % {
				'static_url': settings.STATIC_URL, 'version': version, 'theme': theme}

	res	 = settings.JQUERYUI_LINK_TAG % {'url': url}
	return TextNode(res)


