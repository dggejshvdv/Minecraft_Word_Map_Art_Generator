import json
import os
import locale

class I18N:
    def __init__(self):
        self.current_lang = self.get_system_language()
        self.translations = {}
        self.load_translations()
    
    def get_system_language(self):
        try:
            lang, _ = locale.getdefaultlocale()
            if lang:
                if lang.startswith('zh'):
                    return 'zh_cn'
                return 'en'
        except:
            pass
        return 'en'
    
    def load_translations(self):
        i18n_dir = os.path.join(os.path.dirname(__file__), 'i18n')
        
        if not os.path.exists(i18n_dir):
            os.makedirs(i18n_dir)
        
        for lang in ['zh_cn', 'en']:
            file_path = os.path.join(i18n_dir, f'{lang}.json')
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                except Exception as e:
                    print(f"Error loading translation file {file_path}: {e}")
                    self.translations[lang] = {}
            else:
                self.translations[lang] = {}
    
    def set_language(self, lang):
        if lang in self.translations:
            self.current_lang = lang
            return True
        return False
    
    def t(self, key, **kwargs):
        lang_data = self.translations.get(self.current_lang, {})
        if key in lang_data:
            text = lang_data[key]
            try:
                return text.format(**kwargs)
            except:
                return text
        return key
    
    def get_available_languages(self):
        return list(self.translations.keys())
    
    def get_current_language(self):
        return self.current_lang

_i18n = I18N()

def set_language(lang):
    return _i18n.set_language(lang)

def t(key, **kwargs):
    return _i18n.t(key, **kwargs)

def get_current_language():
    return _i18n.get_current_language()

def get_available_languages():
    return _i18n.get_available_languages()