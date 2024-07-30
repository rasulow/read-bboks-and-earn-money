JAZZMIN_SETTINGS = {
    'site_title': 'OnlineLib',

    'site_header': 'OnlineLib',

    'site_brand': 'OnlineLib',

    # 'site_logo': '',

    # 'login_logo': '',

    'site_logo_classes': 'img-circle',

    # 'site_icon': '',

    'welcome_sign': 'Onlaýn kitaphana hoş geldiňiz!',

    'copyright': 'OnlineLib',

    'search_model': [],

    'user_avatar': None,

    # 'topmenu_links': [
    #     {'name': 'Home', 'url': 'admin:index', 'permissions': ['auth.view_user']},
    #     {'model': 'auth.User'},
    #     {'app': 'Post'}
    # ],

    'usermenu_links': [
        {'model': 'auth.User'}
    ],

    'show_sidebar': True,

    'navigation_expanded': True,

    'hide_apps': [],

    'hide_models': [],

    # 'order_with_respect_to': ['auth', 'Post'],

    # 'custom_links': {
    #     'Post': [
    #         {
    #             'name': 'Make messages',
    #             'icon': 'fas fa-comments',
    #             'permissions': ['Post']
    #         }
    #     ]
    # },

    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.User': 'fas fa-user',
        'auth.Group': 'fas fa-users'
    },

    'default_icon_parents': 'fas fa-chevron-circle-right',

    'default_icon_children': 'fas fa-circle',

    'related_modal_active': True,

    'custom_css': None,

    'custom_js': None,

    'use_google_fonts_cdn': True,

    'show_ui_builder': False,

    'changeform_format': 'horizontal_tabs',

    # 'changeform_format_overrides': {'auth.User': 'collapsible', 'auth.Group': 'vertical_tabs'},

    # 'language_chooser': True,

    'pagination': {
        'per_page': 5,
    },
}