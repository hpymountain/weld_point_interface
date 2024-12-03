SUBSCRIPTIONS = dict(
  green_mobile_s='GreenMobil S',
  green_mobile_m='GreenMobil M',
  green_mobile_l='GreenMobil L',
)

RAN_TYPES = {
  '2g': dict(desc='2G (GSM)', max_throughput_desc='Weak Connection', kbyte_sec=0),
  '3g': dict(desc='3G (HSPA)', max_throughput_desc='20 Mbit/s', kbyte_sec=20*1000/8),
  '4g': dict(desc='4G (LTE)', max_throughput_desc='300 Mbit/s', kbyte_sec=300*1000/8),
}

TERMINAL_TYPES = dict(
  phair_phone=dict(desc='PhairPhone', max_ran_type_idx=1),
  pear_aphone_4s=dict(desc='Pear aphone 4s', max_ran_type_idx=1),
  samsung_s42plus=dict(desc='Samsung S42plus', max_ran_type_idx=2),
)

SIGNAL_QUALITIES = {
  0.5: '50%',
  0.25: '25%',
  0.1: '10%',
  0: '0%',
}

SERVICE_TYPES = dict(
    call=dict(desc='Voice call', min_throughput_kbytes_per_sec=0),
    browse=dict(desc='Browsing', min_throughput_kbytes_per_sec=2*1000/8),
    download=dict(desc='Download', min_throughput_kbytes_per_sec=10*1000/8),
    video=dict(desc='Video', min_throughput_kbytes_per_sec=75*1000/8),
)

SERVICE_MAX_DURATION_MINUTES = 300
