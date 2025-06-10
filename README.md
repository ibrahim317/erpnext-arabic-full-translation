# Arabic Translations for Frappe & ERPNext

[![Translation status](https://img.shields.io/badge/translation-100%25-brightgreen)](.)

This repository contains the complete Arabic translation files (`.po`) for the Frappe Framework and ERPNext. Our goal is to provide a fully localized and seamless experience for Arabic-speaking users of these powerful open-source platforms.

---

## About This Project

This project is dedicated to providing and maintaining high-quality Arabic translations for Frappe and ERPNext. As the official translations can sometimes lag behind or be incomplete, this repository offers a 100% translated alternative.

---

## Supported Versions

It is crucial to use the correct translation files for your specific Frappe and ERPNext versions to avoid any potential issues. These translation files are compatible with the following versions:

* **Frappe Framework Version:** `<= 16.0.0`
* **ERPNext Version:** `<= 16.0.0`

---

## Installation & Usage

To apply these Arabic translations to your Frappe/ERPNext instance, you will need to have access to the command line on your server and have the `bench` command-line utility installed.

Follow these steps carefully:

1.  **Download the translation files:**
    You can either clone this repository or download the `.po` files directly.

    ```bash
    git clone https://github.com/ibrahim317/erpnext-arabic-full-translation
    ```

2.  **Locate your Frappe and ERPNext app directories:**
    The translation files need to be placed in the correct `locale` directory within each app. The typical paths are:
    * **Frappe:** `frappe-bench/apps/frappe/frappe/locale`
    * **ERPNext:** `frappe-bench/apps/erpnext/erpnext/locale`

3.  **Copy the `.po` files:**
    * Copy the `ar.po` file for Frappe to the `frappe-bench/apps/frappe/frappe/locale/` directory.
    * Copy the `ar.po` file for ERPNext to the `frappe-bench/apps/erpnext/erpnext/locale/` directory.

4.  **Update Translations:**
    Navigate to your `frappe-bench` directory and run the following commands to update the translations in your database:

    ```bash
    cd frappe-bench
    bench build
    ```
    This command compiles assets, including your new translation files.

5.  **Clear Cache and Restart:**
    For the changes to take full effect, clear the cache and restart the bench.

    ```bash
    bench --site all clear-cache
    bench restart
    ```

6.  **Set Language for Users:**
    Each user can set their language to Arabic in their user settings within the ERPNext desk.

---

## How to Contribute

We welcome contributions to improve these translations further! Even though the files are 100% translated, there might be typos, better contextual translations, or new strings in future Frappe/ERPNext updates.

You can contribute in the following ways:

* **Reporting Issues:** If you find any mistakes or parts that are not translated correctly, please open an issue in this repository. Describe the issue in detail and, if possible, provide a screenshot.
* **Suggesting Improvements:** You can fork this repository, make your changes to the `.po` files, and then create a pull request. Please ensure you have tested your changes before submitting.

---

## Acknowledgments

A big thank you to all the contributors who have dedicated their time and effort to make these Arabic translations possible.

---

## Contact

If you have any questions or need further assistance, feel free to open an issue in this repository.
