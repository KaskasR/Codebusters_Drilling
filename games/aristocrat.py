# games/aristocrat.py
#!/usr/bin/env python3
"""
games/aristocrat.py

Core logic for an Aristocrat substitution-cipher game,
refactored for Flask (no Tkinter). Supports multi-word
phrases and apostrophes, with dynamic frequency hints from quotes.
"""

import os
import random
import string
import collections
from typing import List, Dict, Optional

import openpyxl


class AristocratGame:
    """Logic for an Aristocrat cipher word-guessing game."""
    def __init__(
        self,
        words_file: str,
        quotes_file: str = "data/English_Quotes.xlsx"
    ):
        self.words_file = words_file
        self.quotes_file = quotes_file
        self.words: List[str] = self._load_words()
        self.quotes: List[str] = self._load_quotes()
        self.plaintext: str = ""
        self.cipher_map: Dict[str, str] = {}
        self.cipher_tokens: List[str] = []
        self.token_frequencies: List[Optional[int]] = []

    def _load_words(self) -> List[str]:
        if not os.path.exists(self.words_file):
            raise FileNotFoundError(f"Word file not found: {self.words_file}")
        with open(self.words_file, encoding="utf-8") as f:
            entries = [line.strip() for line in f if line.strip()]
        if not entries:
            raise ValueError("Word list is empty")
        return entries

    def _load_quotes(self) -> List[str]:
        if not os.path.exists(self.quotes_file):
            raise FileNotFoundError(f"Quotes file not found: {self.quotes_file}")
        try:
            wb = openpyxl.load_workbook(self.quotes_file, read_only=True)
        except Exception as e:
            raise RuntimeError(f"Failed to open quotes file: {e}")
        sheet = wb.active
        quotes: List[str] = []
        for row in sheet.iter_rows(min_row=2, max_col=1, values_only=True):
            cell = row[0]
            if isinstance(cell, str) and cell.strip():
                quotes.append(cell.strip())
        if not quotes:
            raise ValueError("No quotes found in Excel file")
        return quotes

    def _generate_dynamic_frequency_map(self, sample_size: int = 50) -> Dict[str, int]:
        sample = random.choices(self.quotes, k=sample_size)
        text = "".join(sample).upper()
        counts = collections.Counter(ch for ch in text
                                     if ch in string.ascii_uppercase)
        total = sum(counts.values()) or 1
        return {
            letter: max(1, int(counts.get(letter, 0) / total * 100))
            for letter in string.ascii_uppercase
        }

    def generate_cipher(self) -> None:
        raw = random.choice(self.words)
        self.plaintext = raw.upper()

        letters = list(string.ascii_uppercase)
        while True:
            shuffled = letters.copy()
            random.shuffle(shuffled)
            if all(src != dst for src, dst in zip(letters, shuffled)):
                break
        self.cipher_map = dict(zip(letters, shuffled))

        freq_map = self._generate_dynamic_frequency_map()

        self.cipher_tokens.clear()
        self.token_frequencies.clear()
        for ch in self.plaintext:
            if ch in string.ascii_uppercase:
                self.cipher_tokens.append(self.cipher_map[ch])
                self.token_frequencies.append(freq_map[ch])
            elif ch == "'":
                self.cipher_tokens.append("'")
                self.token_frequencies.append(None)
            elif ch.isspace():
                self.cipher_tokens.append("")
                self.token_frequencies.append(None)
            else:
                self.cipher_tokens.append(ch)
                self.token_frequencies.append(None)

    def get_cipher_tokens(self) -> List[str]:
        return self.cipher_tokens

    def get_token_frequencies(self) -> List[Optional[int]]:
        return self.token_frequencies

    def check_guess(self, guess: str) -> bool:
        return guess.strip().upper() == self.plaintext
