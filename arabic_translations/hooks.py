app_name = "arabic_translations"
app_title = "Arabic Translations"
app_publisher = "ibrahim317"
app_description = "Complete Arabic translations for Frappe, ERPNext and HRMS (v15 & v16)"
app_email = "i.aboelsoud21@gmail.com"
app_license = "mit"

# Installation
# ------------
# after_install (not before_install): the overlay catalog can only be compiled
# once the app is registered on the bench.
after_install = "arabic_translations.utils.after_install"
before_uninstall = "arabic_translations.utils.before_uninstall"

# Re-apply whenever another app is installed (it may ship its own ar.po/ar.csv
# that would otherwise shadow or stale-out ours), and after every migrate so
# `bench update` cannot silently drop the translations.
after_app_install = "arabic_translations.utils.after_app_install"
after_app_uninstall = "arabic_translations.utils.after_app_uninstall"
after_migrate = "arabic_translations.utils.after_migrate"
