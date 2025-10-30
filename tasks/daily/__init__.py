from tasks.daily.rhuna_drission import rhuna_drission
from tasks.daily.billions_drission import billions_drission
from tasks.daily.nitrograph_drission import nitrograph_drission
from tasks.daily.overnads_drission import overnads_drission
from tasks.daily.sosovalue_drission import sosovalue_drission

tasks = [
    ('rhuna', rhuna_drission),
    ('billions', billions_drission),
    ('nitrograph', nitrograph_drission),
    ('overnads', overnads_drission),
    ('sosovalue', sosovalue_drission),
]
