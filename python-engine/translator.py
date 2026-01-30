#!/usr/bin/env python3
"""
离线翻译模块 - 使用 Helsinki-NLP OPUS-MT 模型（稳定可靠）
使用本地模型进行多语言翻译，无需联网
"""

from transformers import AutoModelForSeq2SeqLM, MarianTokenizer
import torch

class OfflineTranslator:
    """离线翻译器 - 使用 OPUS-MT 模型"""

    # OPUS-MT 模型映射（经过测试的模型）
    OPUS_MODELS = {
        "zh-en": "Helsinki-NLP/opus-mt-zh-en",  # 中文 → 英文
        "en-zh": "Helsinki-NLP/opus-mt-en-zh",  # 英文 → 中文
        "en-ja": "Helsinki-NLP/opus-mt-en-ja",  # 英文 → 日文
        "ja-en": "Helsinki-NLP/opus-mt-ja-en",  # 日文 → 英文
        "en-ko": "Helsinki-NLP/opus-mt-en-ko",  # 英文 → 韩文
        "ko-en": "Helsinki-NLP/opus-mt-ko-en",  # 韩文 → 英文
        "en-fr": "Helsinki-NLP/opus-mt-en-fr",  # 英文 → 法文
        "fr-en": "Helsinki-NLP/opus-mt-fr-en",  # 法文 → 英文
        "en-de": "Helsinki-NLP/opus-mt-en-de",  # 英文 → 德文
        "de-en": "Helsinki-NLP/opus-mt-de-en",  # 德文 → 英文
        "en-es": "Helsinki-NLP/opus-mt-en-es",  # 英文 → 西班牙文
        "es-en": "Helsinki-NLP/opus-mt-es-en",  # 西班牙文 → 英文
    }

    def __init__(self, source_lang="zh", target_lang="en"):
        """
        初始化翻译器

        Args:
            source_lang: 源语言代码 (zh, en, ja, ko, fr, de, es)
            target_lang: 目标语言代码 (zh, en, ja, ko, fr, de, es)
        """
        self.source_lang = source_lang
        self.target_lang = target_lang

        # 构建模型名称
        lang_pair = f"{source_lang}-{target_lang}"
        if lang_pair in self.OPUS_MODELS:
            self.model_name = self.OPUS_MODELS[lang_pair]
        else:
            raise ValueError(f"不支持的语言对: {lang_pair}")

        self.tokenizer = None
        self.model = None

    def load_model(self):
        """加载翻译模型（首次会自动下载）"""
        if self.model is None:
            print(f"正在加载翻译模型: {self.model_name}")
            print(f"翻译方向: {self.source_lang} → {self.target_lang}")
            print("提示：首次运行会下载模型文件（约 300 MB）")
            print()

            try:
                # 加载 tokenizer 和模型
                self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

                print(f"✓ 模型加载完成")
                print()
            except Exception as e:
                print(f"✗ 模型加载失败: {e}")
                raise

    def translate(self, text, src_lang=None, tgt_lang=None):
        """
        翻译文本

        Args:
            text: 要翻译的文本
            src_lang: 源语言（可选，默认使用初始化时的设置）
            tgt_lang: 目标语言（可选，默认使用初始化时的设置）

        Returns:
            翻译后的文本
        """
        if self.model is None:
            self.load_model()

        # 编码输入文本
        inputs = self.tokenizer(text, return_tensors="pt")

        # 生成翻译
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=128,  # 合理的长度限制
                num_beams=4,
                no_repeat_ngram_size=2,
                early_stopping=True
            )

        # 解码结果
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result


class TranslationManager:
    """翻译管理器 - 管理 OPUS-MT 翻译器"""

    def __init__(self):
        """初始化翻译管理器"""
        self.translators = {}

    def get_translator(self, source_lang, target_lang):
        """
        获取指定语言对的翻译器

        Args:
            source_lang: 源语言
            target_lang: 目标语言

        Returns:
            OfflineTranslator 实例
        """
        lang_pair = f"{source_lang}-{target_lang}"
        if lang_pair not in self.translators:
            print(f"创建翻译器: {source_lang} → {target_lang}")
            self.translators[lang_pair] = OfflineTranslator(source_lang, target_lang)

        return self.translators[lang_pair]

    def translate(self, text, source_lang, target_lang):
        """
        翻译文本

        Args:
            text: 要翻译的文本
            source_lang: 源语言
            target_lang: 目标语言

        Returns:
            翻译后的文本
        """
        translator = self.get_translator(source_lang, target_lang)
        return translator.translate(text)


# 便捷函数
def translate_zh_to_en(text):
    """中文转英文"""
    translator = OfflineTranslator(source_lang="zh", target_lang="en")
    return translator.translate(text)


def translate_en_to_zh(text):
    """英文转中文"""
    translator = OfflineTranslator(source_lang="en", target_lang="zh")
    return translator.translate(text)


# 支持的语言（基于 OPUS-MT 模型）
SUPPORTED_LANGUAGES = {
    "zh": {"name": "中文", "targets": ["en"]},
    "en": {"name": "英文", "targets": ["zh", "ja", "ko", "fr", "de", "es"]},
    "ja": {"name": "日文", "targets": ["en"]},
    "ko": {"name": "韩文", "targets": ["en"]},
    "fr": {"name": "法文", "targets": ["en"]},
    "de": {"name": "德文", "targets": ["en"]},
    "es": {"name": "西班牙文", "targets": ["en"]},
}


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("离线翻译测试")
    print("=" * 60)
    print()

    # 测试中文 → 英文
    print("测试 1: 中文 → 英文")
    try:
        zh_text = "你好，世界！"
        print(f"原文: {zh_text}")
        en_result = translate_zh_to_en(zh_text)
        print(f"译文: {en_result}")
        print("✓ 测试通过")
        print()
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        print()

    # 测试英文 → 中文
    print("测试 2: 英文 → 中文")
    try:
        en_text = "Hello, world!"
        print(f"原文: {en_text}")
        zh_result = translate_en_to_zh(en_text)
        print(f"译文: {zh_result}")
        print("✓ 测试通过")
        print()
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        print()

    print("=" * 60)
    print("测试完成")
    print("=" * 60)
