import pytest
from engine.strategies import FastStrategy, BalancedStrategy, MaxCompressionStrategy


def test_fast_strategy_compression():
    strategy = FastStrategy()
    options = strategy.get_options()
    assert options.gs_preset == "printer"


def test_balanced_strategy_compression():
    strategy = BalancedStrategy()
    options = strategy.get_options()
    assert options.gs_preset == "ebook"


def test_max_compression_strategy_compression():
    strategy = MaxCompressionStrategy()
    options = strategy.get_options()
    assert options.gs_preset == "screen"

