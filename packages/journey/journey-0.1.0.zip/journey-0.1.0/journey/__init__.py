from pkg_resources import iter_entry_points
from .system import System

def import_all_quest_hooks():
    for ep in iter_entry_points('journey_hooks', 'hook'):
        ep.load()