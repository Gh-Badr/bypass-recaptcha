# Bypass-reCAPTCHA
## Description
This project is a proof of concept showing how AI can be used for malicious purposes. It uses a custom GPT model to bypass the [Google reCAPTCHA v2](https://www.google.com/recaptcha/about/) challenge (The image selection one). The idea is to use the model to generate a response to the reCAPTCHA challenge and then use the generated response to bypass the reCAPTCHA.

## Team Members

- FIALI Mouad
- GHAZAOUI Badr
- MAROUANE Kamal
- RIMAOUI Nabila
- ZARKTOUNI Ismail

## Table of Contents
- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Requirements](#requirements)
- [Usage](#usage)
- [Ethical Considerations](#ethical-considerations)

## Requirements
- [ChatGPT - Plus](https://openai.com/blog/chatgpt-plus) | This project is using the a custom GPT model created by our team which is [GridVision](https://chat.openai.com/g/g-K30O0wu7c-grid-vision). This model can only be accessed if you have a valid ChatGPT - Plus subscription.

- Clone this repository and navigate to the project directory using
``` bash
git clone
cd bypass-recaptcha
```

- (Facultative) Create a virtual environment using
``` python
python -m venv venv
```

- All the required packages are listed in the [`requirements.txt`](requirements.txt) file. You can install them using
``` python
pip install -r requirements.txt
```

## Usage
- Before running the main script, you need to set the variables `user-data-dir` and `profile-directory` in the [`config.yml`](config/config.yml) file. 

    You can find the needed values by going to `chrome://version` in your browser. The `user-data-dir` is the path to the `User Data` folder and the `profile-directory` is the name of the profile folder.

    **Note:** The required profile is the one which you have your chatgpt-plus connected to. If you don't have a profile connected to chatgpt-plus, you can create a new profile and connect it to chatgpt-plus.

- Once you have set the variables, you can run the main script using 
``` python
python main.py
```

## Ethical Considerations
Even if this project is only a proof of concept, showing how AI can be used for malicious purposes, and the results were not very useful as the bot was not able to completely bypass the reCAPTCHA, we still want to highlight that It is for educational purposes only. We do not encourage the use of this project or Its ideas for any malicious purposes. We are not responsible for any misuse of this project.
