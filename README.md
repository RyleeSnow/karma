# My Utility Library

This repository contains a collection of utility functions and scripts that I frequently use in my projects. The library is designed to simplify data processing, logging, notifications, and more. It is primarily intended for personal use, but feel free to explore and adapt it for your own needs.

## Features

- **Data Reading and Writing**: Functions to read and write data in various formats such as CSV, Excel, and Parquet.
- **Data Transformation**: Utilities to transform data types within pandas DataFrames.
- **Logging**: Set up a logger to output logs to the console and optionally to a file.
- **Notifications**: Send notifications via WeChat and email.
- **Miscellaneous Utilities**: Includes functions for multiprocessing, YAML file reading, and list/set operations.

## Installation

To use this library:
1. clone the repository to your local machine
2. install by pip: `pip install dwoht`

## Usage

### Data Reading and Writing

- **Read Data**: Use `read_small_data` or `read_big_data` to read data files with support for different formats and options for column renaming and reformatting.
- **Save Data**: Use `save_data` to save pandas DataFrames to various file formats.

### Data Transformation

- **Column Conversion**: Use `col_to_str` and `col_to_float` to convert DataFrame columns to string or float types, respectively.

### Notifications

- **WeChat Notification**: Use `wechat_notification` to send messages via WeChat.
- **Email Notification**: Use `email_notification` to send emails using SMTP.

### Logging

- **Set Logger**: Use `set_logger` to configure a logger for your application, with options to save logs to a file.

### Miscellaneous Utilities

- **Multiprocessing**: Use `dataframe_mp` to apply a function to a DataFrame using multiple CPU cores.
- **YAML Reading**: Use `yaml_to_object` to read YAML configuration files into Python objects.
- **List and Set Operations**: Functions like `list_intersection`, `list_diff`, `set_union`, etc., for common list and set operations.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
