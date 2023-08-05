import nomad
import numpy as np

# This was a one-time use script to confirm that the RA swatch ranges are >= and <.

#  Found:
# LOW MATCH:
# 0021 18.0 18.0 18.2499899074
# LOW MATCH:
# 0064 15.25 15.25 15.4999305556
# LOW MATCH:
# 73 4.75 4.75 4.99976037037
# before I then cut off the run.  Good enough for me, showing that
# RA swatch ranges are >= and <
# (which makes logical sense)


for cur_dec_filenum in np.arange(1799):
    nomad_filenum_str = '%04i' % cur_dec_filenum
    print nomad_filenum_str
    for ra_swatch in np.arange(0, 24, 0.25):
        records_to_retrieve = nomad._determine_record_numbers_to_retrieve(ra_swatch, ra_swatch, cur_dec_filenum)[0]
        f = open(nomad._nomad_dir + nomad_filenum_str[0:3] + '/m' + nomad_filenum_str + '.cat', 'rb')
        f.seek((records_to_retrieve[0] - 1) * nomad._nomad_record_length_bytes)
        raw_byte_data = f.read((records_to_retrieve[1] - records_to_retrieve[0] + 1) * nomad._nomad_record_length_bytes)
        nomad_ids = [nomad_filenum_str + '-' + ('%07i' % a) for a in range(records_to_retrieve[0], records_to_retrieve[1] + 1)]
        stars = nomad._apply_proper_motion(nomad._convert_raw_byte_data_to_dataframe(raw_byte_data, nomad_ids=nomad_ids),
                                           epoch=2000.0)
        if ra_swatch == stars['RAJ2000'].min() / 15.:
            print 'LOW MATCH:'
            print nomad_filenum_str, ra_swatch, stars['RAJ2000'].min() / 15., stars['RAJ2000'].max() / 15.
        if (ra_swatch + 0.25) == stars['RAJ2000'].max() / 15.:
            print 'HIGH MATCH:'
            print nomad_filenum_str, ra_swatch, stars['RAJ2000'].min() / 15., stars['RAJ2000'].max() / 15.
