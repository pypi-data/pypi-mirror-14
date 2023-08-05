#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			December 2008
"""
from setuptools import setup, find_packages
from os import listdir
from os.path import join, isdir

setup(
    name = "woost",
    version = "2.6.2",
    author = "Whads/Accent SL",
    author_email = "tech@whads.com",
    maintainer = "Marti Congost",
    maintainer_email = "marti.congost@whads.com",
    url = "http://woost.info",
    description = "Model driven multilanguage CMS.",
    long_description =
"""Woost is a Content Management System designed from the ground up  to be able
to publish arbitrary data models, including content in multiple languages. Some
of its features include:\n"

    * Use inheritance, relations and validations to define complex models

    * Automatically generate forms and listings for your models from a schema
      description

    * Translate your content into multiple languages, edit translations side by
      side

    * Compatible with lots of popular Python templating engines

    * Place arbitrarily complex access restrictions

    * Extension framework, with several built-in extensions (comments,
      ecommerce, integration with online services, and many others)
""",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: ZODB",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: Catalan",
        "Natural Language :: Spanish",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP :: Site Management"
    ],
    install_requires = [
        "simplejson",
        "enum34",
        "clipboard",
        "cocktail>=1.7,<1.8"
    ],
    extras_require = {
        'campaign_monitor_api': ["campaign_monitor_api"],
        'campaign3': ["createsend"],
        "twitterpublication": ["oauth2"],
        "amazon_s3_static_publication": ["boto"],
        "newsletters": ["premailer"],
        "identity": ["google-api-python-client"]
    },
    packages = find_packages(),
    include_package_data = True,
    entry_points = {
        "woost.extensions": [
            "shop = woost.extensions.shop:ShopExtension",
            "countries = woost.extensions.countries:CountriesExtension",
            "payments = woost.extensions.payments:PaymentsExtension",
            "comments = woost.extensions.comments:CommentsExtension",
            "recaptcha = woost.extensions.recaptcha:ReCaptchaExtension",
            "staticsite = woost.extensions.staticsite:StaticSiteExtension",
            "sitemap = woost.extensions.sitemap:SitemapExtension",
            "pdf = woost.extensions.pdf:PDFExtension",
            "vimeo = woost.extensions.vimeo:VimeoExtension",
			"signup = woost.extensions.signup:SignUpExtension",
            "googlesearch = woost.extensions.googlesearch:GoogleSearchExtension",
            "googleanalytics = woost.extensions.googleanalytics:GoogleAnalyticsExtension",
            "campaignmonitor = woost.extensions.campaignmonitor:CampaignMonitorExtension",
            "mailer = woost.extensions.mailer:MailerExtension",
            "usermodels = woost.extensions.usermodels:UserModelsExtension",
            "locations = woost.extensions.locations:LocationsExtension",
            "webconsole = woost.extensions.webconsole:WebConsoleExtension",
            "blocks = woost.extensions.blocks:BlocksExtension",
            "opengraph = woost.extensions.opengraph:OpenGraphExtension",
            "ecommerce = woost.extensions.ecommerce:ECommerceExtension",
            "facebookpublication = woost.extensions.facebookpublication:FacebookPublicationExtension",
            "shorturls = woost.extensions.shorturls:ShortURLsExtension",
            "twitterpublication = woost.extensions.twitterpublication:TwitterPublicationExtension",
            "textfile = woost.extensions.textfile:TextFileExtension",
            "audio = woost.extensions.audio:AudioExtension",
            "issuu = woost.extensions.issuu:IssuuExtension",
            "campaign3 = woost.extensions.campaign3:CampaignMonitor3Extension",
            "youtube = woost.extensions.youtube:YouTubeExtension",
            "tv3alacarta = woost.extensions.tv3alacarta:TV3ALaCartaExtension",
            "externalfiles = woost.extensions.externalfiles:ExternalFilesExtension",
            "restrictedaccess = woost.extensions.restrictedaccess:RestrictedAccessExtension",
            "annotations = woost.extensions.annotations:AnnotationsExtension",
            "notices = woost.extensions.notices:NoticesExtension",
            "variables = woost.extensions.variables:VariablesExtension",
            "surveys = woost.extensions.surveys:SurveysExtension",
            "newsletters = woost.extensions.newsletters:NewslettersExtension",
            "forms = woost.extensions.forms:FormsExtension",
            "translationworkflow = woost.extensions.translationworkflow:TranslationWorkflowExtension",
            "identity = woost.extensions.identity:IdentityExtension"
        ]
    },
    # Woost can't yet access view resources (images, style sheets, client
    # side scripts, etc) that are packed inside a zipped egg, so distribution
    # in zipped form is disabled
    zip_safe = False
)

