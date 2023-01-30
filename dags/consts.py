import datetime

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
yesterday_unix_timestamp = int(yesterday.timestamp())*1000

URL = 'https://api.spotify.com/v1/me/player/recently-played?after={time}'.format(time=yesterday_unix_timestamp)
TOKEN = 'BQCT-eqEmIpp41C3YflrMxHb0t4WgFXtMdpEDRNZAksRyOHBf1MRi-xt78ynfBLF0SCU0qz_SCHYaK7iZxq_bqdtPghDJeEiMG_Mty5AAeBpYzj-u2Ez8H4Xz_-eM6GEdEtmpaJMjurwDPaReqQxsV2OrrpksCvuWeRaPCuKmNNH4BLj1XHJdNgsdV7HNvYFM1ux5cbP'