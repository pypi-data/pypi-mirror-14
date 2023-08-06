# What is wagtailmenus?

It's an extension for torchbox's [Wagtail CMS](https://github.com/torchbox/wagtail) to help you manage complex multi-level navigation and flat menus in a consistent, flexible way.

## What does it provide?

### 1. Independent control over your root-level main menu items

The `MainMenu` model and it's orderable inline `MainMenuItem`s let you define the root-level items for your site's main navigation (or one for each site, if it's a multi-site project). Your menu items can link to pages or custom URLs, and you can append an optional hash or querystring to the URL if required. You can still hide pages from menus by unchecking `show_in_menus` on the page, but your site's root-level menu items (likely displayed in a manner that is 'sensitive' to change) will be protected from accidental additions.

Your existing `Page` structure powers everything past the root level, so you don't have to recreate your whole page tree elsewhere.

<img alt="Screenshot of MainMenu edit page in Wagtail admin" src="https://raw.githubusercontent.com/rkhleics/wagtailmenus/master/screenshots/wagtailmenus-mainmenu-edit.png" />

### 2. Specify pages that should repeat in dropdown/hover menus, to improve visibility/acessibility

Extend the `MenuPage` class (an abstract sub-class of Wagtail's `Page` model) to create your custom page types, and gain a couple of extra fields that allow you to control advanced menu behaviour on a page-to-page basis.

### 3. Manage multiple 'flat' menus from the Wagtail admin area

Create `FlatMenu`s to help you manage lists of links throughout your project. Each `FlatMenu` will have a unique `handle`, allowing you to reference it in `{% flat_menu %}` tags throughout your project's templates.

<img alt="Screenshot of FlatMenu list page in Wagtail admin" src="https://raw.githubusercontent.com/rkhleics/wagtailmenus/master/screenshots/wagtailmenus-flatmenu-list.png" />

### 4. A set of powerful template tags to render your menus using accessible menu templates

Output from the included templates is designed to be fully accessible and compatible with Bootstrap 3. You can easily use your own templates by passing a `template` variable to any of the tags, or you can override the included templates by putting customised versions in a system-preferred location.

<img alt="Screenshot from Sublime editor showing menu template code" src="https://raw.githubusercontent.com/rkhleics/wagtailmenus/master/screenshots/wagtailmenus-menu-templates.png" />

## How to install

1. Install the package using pip: `pip install wagtailmenus`.
2. Add `wagtailmenus` to `INSTALLED_APPS` in your project settings (after `wagtailmodeladmin` and before your `core` app).
3. Run `python manage.py migrate wagtailmenus` to set up the initial database tables.

**Optional steps, if you wish to use `MenuPage`**

**NOTE:** It is not necessary to extend `MenuPage` for all custom page types; Just ones you know will be used for pages that may have children, and will need the option to repeat themselves in sub-menus when listing those children.

1. In your `core` app and other apps (wherever you have defined a custom page/content model to use in your project), import `wagtailmenus.models.MenuPage` and extend that instead of `wagtail.wagtailcore.models.Page`.
2. Run `python manage.py makemigrations` to create migrations for the apps you've updated.
3. Run `python manage.py migrate` to add apply those migrations.

## How to use

**Skip to:**

1. [Defining root-level main menu items in the CMS](#defining-main-menu-items)
2. [Using the `{% main_menu %}` tag](#main-menu-tag)
3. [Defining flat menus in the CMS](#defining-flat-menus)
4. [Using the `{% flat_menu %}` tag](#flat-menu-tag)
5. [Using the `{% section_menu %}` tag](#section-menu-tag)
6. [Using the `{% children_menu %}` tag](#children-menu-tag)
7. [Optional repetition of selected pages in menus using `MenuPage`](#using-menupage)
8. [Changing the default settings](#changing-defaults)

### <a id="defining-main-menu-items"></a>1. Defining root-level main menu items in the CMS

1. Log into the Wagtail CMS for your project (as a superuser).
2. Click on `Settings` in the side menu to access the options in there, then select `Main menu`.
3. You'll be automatically redirected to the `Main menu` edit page for the current site (or the 'default' site, if the current site cannot be identified). For multi-site projects, a 'site switcher' will appear in the top right, allowing you to edit main menus for each site.
4. Use the **MENU ITEMS** inline panel to define the root-level items, and save your changes when finished.

### <a id="main-menu-tag"></a>2. Using the `{% main_menu %}` tag

The `{% main_menu %}` tag allows you to display the `MainMenu` defined for the current site in your Wagtail project, with CSS classes automatically applied to each item to indicate the current page or ancestors of the current page. It also does a few sensible things, like never adding the 'ancestor' class for a homepage link, or outputting children for it.

1. In whichever template you want your main menu to appear, load `menu_tags` using `{% load menu_tags %}`.
2. Use the `{% main_menu %}` tag where you want the menu to appear.

**Optional params for `{% main_menu %}`**

- **`show_multiple_levels`** (default: `True`): Lets you control whether subsequent levels should be rendered. If you only want to display the root-level items, you should add `show_multiple_levels=False` for improved speed and efficiency (it will prevent wagtailmenus from doing unnecessary/expensive checks to work out if each page has children).
- **`allow_repeating_parents`** (default: `True`): If set to False, will ignore any repetition-related settings for individual pages, and not repeat any pages when rendering.
- **`apply_active_classes`** (default: `True`): wagtailmenus will attempt to add 'active' and 'ancestor' classes to the menu items (based on the current page). To disable this behaviour, add `apply_active_classes=False`. Doing so will improve speed and efficiency (it will prevent wagtailmenus from doing unnecessary checks to work out which classes to use for each page)
- **`template`** (default: `'menus/main_menu.html'`): Lets you render the menu to a template of your choosing.

### <a id="defining-flat-menus"></a>3. Defining flat menus in the CMS

1. Log into the Wagtail CMS for your project (as a superuser).
2. Click on `Settings` in the side menu to access the options in there, then select `Flat menus`.
3. Click the button at the top of the page to add a flat menu for your site (or one for each of your sites if you are running a multi-site setup). <img alt="Screenshot indicating the location of the add button on the FlatMenu list page" src="https://raw.githubusercontent.com/rkhleics/wagtailmenus/master/screenshots/wagtailmenus-flatmenu-add.png" />
4. Fill out the form, choosing a 'unique for site' `handle` to reference in your templates, and using the **MENU ITEMS** inline panel to define the links you want the menu to have. Save your changes when finished. <img alt="Screenshot showing the FlatMenu edit interface" src="https://raw.githubusercontent.com/rkhleics/wagtailmenus/master/screenshots/wagtailmenus-flatmenu-edit.png" />

### <a id="flat-menu-tag"></a>4. Using the `{% flat_menu %}` tag

1. In whichever template you want your menu to appear, load `menu_tags` using `{% load menu_tags %}`.
2. Use the `{% flat_menu 'menu-handle' %}` tag where you want the menu to appear, where 'menu-handle' is the unique handle for the menu you added.

**Optional params for `{% flat_menu %}`**

- **`show_menu_heading`** (default: `True`): Passed through to the template used for rendering, where it can be used to conditionally display a heading above the menu.
- **`apply_active_classes`** (default: `False`): If you wish for wagtailmenus to attempt to add 'active' and 'ancestor' classes to the menu items (based on the current page), add `apply_active_classes=True`.
- **`template`** (default: `'menus/flat_menu.html'`): Lets you render the menu to a template of your choosing.

### <a id="section-menu-tag"></a>5. Using the `{% section_menu %}` tag

The `{% section_menu %}` tag allows you to display a context-aware, page-driven menu in your Wagtail project, with CSS classes automatically applied to each item to indicate the current page or ancestors of the current page.  

1. In whichever template you want the section menu to appear, load `menu_tags` using `{% load menu_tags %}`.
2. Add `{% section_menu %}` where you want the menu to appear.

**Optional params for `{% section_menu %}`**

- **`show_section_root`** (default: `True`): Passed through to the template used for rendering, where it can be used to conditionally display the root page of the current section.
- **`show_multiple_levels`** (default: `True`): If you only want to display a single level of pages, you should add `show_multiple_levels=False` for improved speed and efficiency (it will prevent wagtailmenus from doing unnecessary/expensive checks to work out if each page has children).
- **`allow_repeating_parents`** (default: `True`): If set to False, will ignore any repetition-related settings for individual pages, and not repeat any pages when rendering.
- **`apply_active_classes`** (default: `True`): wagtailmenus will attempt to add 'active' and 'ancestor' classes to the menu items (based on the current page). To disable this behaviour, add `apply_active_classes=False`. Doing so will improve speed and efficiency (it will prevent wagtailmenus from doing unnecessary checks to work out which classes to use for each page).
- **`template`** (default: `'menus/section_menu.html'`): Lets you render the menu to a template of your choosing.

### <a id="children-menu-tag"></a>6. Using the `{% children_menu %}` tag

The `{% children_menu %}` tag is used in main menu and section menu templates to render menu items past the first level, but there's no reason it can't be used in places where you have a page in the context, and wish to display a menu just for it's children (or even further down the tree, if desired).

1. In whichever template you want the menu to appear, load `menu_tags` using `{% load menu_tags %}`.
2. Use the `{% children_menu parent_page %}` tag where you want the menu to appear, where `parent_page` is a Page object that you wish to display children for (the current page should be available as `self` in the context, if you're rendering a page).

**Optional params for `{% children_menu %}`**

- **`stop_at_this_level`** (default: `False`): If you only want to display a single level of pages, you should add `stop_at_this_level=True` for improved speed and efficiency (it will prevent wagtailmenus from doing unnecessary/expensive checks to work out if each page has children).
- **`apply_active_classes`** (default: `True`): wagtailmenus will attempt to add 'active' and 'ancestor' classes to the menu items (based on the current page). To disable this behaviour, add `apply_active_classes=False` ). Doing so will improve speed and efficiency (it will prevent wagtailmenus from doing unnecessary checks to work out which classes to use for each page).
- **`template`** (default: `'menus/children_menu.html'`): Lets you render the menu to a template of your choosing.

### <a id="using-menupage"></a>7. Optional repetition of selected pages in menus using `MenuPage`

Let's say you have an 'About Us' section on your site. The top-level 'About Us' page has a decent amount of important content on it, and it also has important children pages that have more specific content (e.g. 'Meet the team', 'Our mission and values', 'Staff vacancies'). You want people to be able to access the top-level 'About Us' page from your navigation as easily as the other pages, but you're using a drop-down menu, and the 'About Us' page link has simply become a toggle for hiding and showing its children pages.

Presuming the 'About Us' page uses a model that extends `wagtailmenus.models.MenuPage`:

1. Edit the 'About Us' page in the CMS, and click on the `Settings` tab.
2. Uncollapse the `ADVANCED MENU BEHAVIOUR` panel by clicking the downward-pointing arrow next to the panel's label. <img alt="Screenshot showing the collapsed 'advanced menu behaviour' panel" src="https://raw.githubusercontent.com/rkhleics/wagtailmenus/master/screenshots/wagtailmenus-menupage-settings-collapsed.png" />
4. Tick the **Repeat in sub-navigation** checkbox that appears, and publish your changes. <img alt="Screenshot show the expanded 'advanced menu behaviour' panel" src="https://github.com/rkhleics/wagtailmenus/blob/master/screenshots/wagtailmenus-menupage-settings-visible.png" />

In a multi-level the main menu or section menu, an additional link to the 'About Us' page should now appear as the first item alongside links to it's children pages, allowing that page to be accessed more easily. The page's title will be used as the link text for the repeated item by default. But, it's often desirable to use something different (e.g. 'Overview' or 'Section home'). You can do this using the **Repeated item link text** field.

### <a id="changing-settings"></a>8. Changing the default settings

You can override some of wagtailmenus' default behaviour by adding one of more of the following to your project's settings:

- **`WAGTAILMENUS_ACTIVE_CLASS`** (default: `'active'`): The class added to menu items for the currently active page (when using a menu template with `apply_active_classes=True`)
- **`WAGTAILMENUS_ACTIVE_ANCESTOR_CLASS`** (default: `'ancestor'`): The class added to any menu items for pages that are ancestors of the currently active page (when using a menu template with `apply_active_classes=True`)
- **`WAGTAILMENUS_MAINMENU_MENU_ICON`** (default: `'list-ol'`): Use this to change the icon used to represent `MainMenu` in the Wagtail admin area.
- **`WAGTAILMENUS_FLATMENU_MENU_ICON`** (default: `'list-ol'`): Use this to change the icon used to represent `FlatMenu` in the Wagtail admin area.
- **`WAGTAILMENUS_DEFAULT_MAIN_MENU_TEMPLATE`** (default: `'menus/main_menu.html'`): The name of the template used for rendering by the `{{ main_menu }}` tag when `template` isn't specified as a keyword argument.
- **`WAGTAILMENUS_DEFAULT_FLAT_MENU_TEMPLATE`** (default: `'menus/flat_menu.html'`): The name of the template used for rendering by the `{{ flat_menu }}` tag when `template` isn't specified as a keyword argument.
- **`WAGTAILMENUS_DEFAULT_SECTION_MENU_TEMPLATE`** (default: `'menus/section_menu.html'`): The name of the template used for rendering by the `{{ section_menu }}` tag when `template` isn't specified as a keyword argument.
- **`WAGTAILMENUS_DEFAULT_CHILDREN_MENU_TEMPLATE`** (default: `'menus/children_menu.html'`): The name of the template used for rendering by the `{{ childre_menu }}` tag when `template` isn't specified as a keyword argument.
