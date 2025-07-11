from chrome_extensions.x import x_detect
from chrome_extensions.discord import discord_detect
from chrome_extensions.yescaptcha import yescaptcha_drission
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
from tasks.ruffie_drission import ruffie_drission
from tasks.goblin_meme_drission import goblin_meme_drission
from tasks.monadscore_drission import monadscore_drission
from tasks.shelby_drission import shelby_drission
from tasks.pharosnetwork_drission import pharosnetwork_drission
from tasks.wardenprotocol_drission import wardenprotocol_drission
from tasks.onefootball_drission import onefootball_drission
from tasks.zkverify import zkverify_drission
from tasks.sosovalue_drission import sosovalue_drission
from tasks.assisterr_drission import assisterr_drission
from tasks.nebulai_drission import nebulai_drission
from tasks.vibes_drission import vibes_drission
from tasks.snoonaut_drission import snoonaut_drission

tasks = [
    ('assisterr', assisterr_drission)
    ("goblin_meme", goblin_meme_drission)
    ("monadscore", monadscore_drission)
    ("nebulai", nebulai_drission)
    ("onefootball", onefootball_drission)
    ("pharosnetwork", pharosnetwork_drission)
    ("ruffie", ruffie_drission)
    ("snoonaut",snoonaut_drission)
]
